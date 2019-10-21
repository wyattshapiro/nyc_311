# test format()
file_path = '{year}/{month}/{day}/{unique_id}.json'
rendered_file_path = file_path.format(**{"year":"2019", "month":"2019", "day":"2019"}).format(unique_id='1')
print(rendered_file_path)
