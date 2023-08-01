import pandas as pd
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from utils.utils import parse_result_html, calculate_gpa, calculate_cgpa, get_semester, clean
from .forms import ResultUploadForm
from .models import Result




def upload_result_view(request):
    # if a POST request is sent
    if request.method == 'POST':
        form = ResultUploadForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_results = form.cleaned_data["file"]
            user = request.user

            for file in uploaded_results:
                dfs, session, level, fac = parse_result_html(file.file)

                # looping over each semester result in the file
                for df in dfs:
                    semester = get_semester(df)
                    result_id = f'{user.matric}:{session}/{semester}/{level}{"E" if fac == "Engineering and Technology" else ""}'       # unique id to differentiate each result
                    cleaned_df = clean(df, result_id)
                    # checking to see if the result already exists in the database using the `result_id`
                    result = Result.objects.filter(result_id=result_id)

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
                    result.save()
            
            messages.success(request, 'Uploaded successfully')
            # Calculating CGPA at the end of each semester
            user_results = Result.objects.filter(owner=user).order_by('result_id')
            for i, result in enumerate(user_results, start=1):
                prev_dfs = [clean(pd.read_json(r.payload), r.result_id) for r in user_results[:i]]
                result.cgpa = calculate_cgpa(prev_dfs)
                result.save()
            user.cgpa = result.cgpa
            user.save()
            return redirect(reverse('accounts:dashboard'))
        form = ResultUploadForm(request.POST, request.FILES)
    # otherwise;
    else:
        form = ResultUploadForm()
    return render(request, 'results/upload.html', {'form': form})
