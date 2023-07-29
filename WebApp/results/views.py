import pandas as pd
from django.shortcuts import render

from utils.utils import parse_result_html, calculate_gpa, calculate_cgpa, get_semester, clean, merge
from .forms import ResultUploadForm
from .models import Result




def upload_result_view(request):
    # if a POST request is sent
    if request.method == 'POST':
        form = ResultUploadForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_results = form.cleaned_data["file"]
            user = request.user
            user_results = Result.objects.filter(owner=user)

            for file in uploaded_results:
                dfs, session, level, fac = parse_result_html(file.file)

                # looping over each semester result in the file
                for df in dfs:
                    cleaned_df = clean(df, fac, level)
                    semester = get_semester(cleaned_df)
                    result_id = f'{user.matric}:{session}/{semester}'       # unique id to differentiate each result
                    # checking to see if the result already exists in the database using the `result_id`
                    result = user_results.filter(result_id=result_id)
                    prev_payloads = [clean(pd.read_json(result.payload), fac, result.level) for result in user_results if result.result_id < result_id]
                    prev_payloads.append(cleaned_df)

                    # create a new `Result` object if it doesn't exist already
                    if len(result) == 0:
                        result = Result(
                            semester = semester,
                            result_id = result_id,
                            owner = user,
                            level = level,
                            session = session,
                            )
                    # otherwise, update the existing result
                    else:
                        result = result[0]
                    result.payload = df.to_json()
                    result.gpa = calculate_gpa(cleaned_df)
                    result.cgpa = calculate_cgpa(prev_payloads)
                    result.save()
            return render(request, 'results/success.html')
    # otherwise;
    else:
        form = ResultUploadForm()
    return render(request, 'results/upload.html', {'form': form})
