from django.shortcuts import render

from utils.utils import parse_result_html, calculate_gpa, get_semester
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
                dfs, session, level = parse_result_html(file.file)

                # looping over each semester result in the file
                for df in dfs:
                    semester = get_semester(df)
                    result_id = f'{user.matric}:{session}/{semester}'       # unique id to differentiate each result
                    # checking to see if the result already exists in the database using the `result_id`
                    result = Result.objects.filter(result_id=result_id)
                    # create a new `Result` object if it doesn't exist already
                    print('result_id: ', result_id)
                    if len(result) == 0:
                        result = Result(
                            semester = semester,
                            result_id = result_id,
                            owner = user,
                            level = level,
                            session = session,
                            payload = df.to_html(),
                            gpa = calculate_gpa(df),
                            )
                    # otherwise, update the existing result
                    else:
                        result = result[0]
                        result.payload = df.to_html()
                        result.gpa = calculate_gpa(df)
                    result.save()
            return render(request, 'results/success.html')
    # otherwise;
    else:
        form = ResultUploadForm()
    return render(request, 'results/upload.html', {'form': form})
