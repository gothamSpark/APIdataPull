import urllib3
import json
LOCAL_FILE_SYS = []
#S3_BUCKET = "your-s3-bucket"  # please replace with your bucket name
CHUNK_SIZE = 10000  # determined based on API, memory constraints, experimentation



def get_num_records():
    # Dummy function, to replicate GET http://jsonplaceholder.typicode.com/number_of_users call
    return 100000


def get_data(
    start_user_id, end_user_id, get_path="http://jsonplaceholder.typicode.com/posts"
):
    http = urllib3.PoolManager()
    data = {"userId": None, "id": None, "title": None, "body": None}
    try:
        r = http.request(
            "GET",
            get_path,
            retries=urllib3.util.Retry(3),
            fields={"start_user_id": start_user_id, "end_user_id": end_user_id},
        )
        data = json.loads(r.data.decode("utf8").replace("'", '"'))
    except KeyError as e:
        print(f"Wrong format url {get_path}", e)
    except urllib3.exceptions.MaxRetryError as e:
        print(f"API unavailable at {get_path}", e)
    return data


def write_to_local(data, part, loc=LOCAL_FILE_SYS):
    # part = 'part-'
    # file_name = loc + "0000" + str(part)
    # with open(file_name, "w") as file:
    #     for elt in data:
    #         file.write(parse_data(elt))
    # return file_name
    print("stage3")
    print(data)
    loc.append(data)


def download_data(N):
    for i in range(0, N, CHUNK_SIZE):
        data = get_data(i, i + CHUNK_SIZE)
        write_to_local(data, i // CHUNK_SIZE)





def lambda_handler():
    print("stage 1")
    N = get_num_records()
    print('stage 2')
    download_data(N)

    # key = _get_key()
    # files = [f for f in listdir(LOCAL_FILE_SYS) if isfile(join(LOCAL_FILE_SYS, f))]
    # for f in files:
    #     s3_client.upload_file(LOCAL_FILE_SYS + "/" + f, S3_BUCKET, key + f)


lambda_handler()

print(LOCAL_FILE_SYS)
