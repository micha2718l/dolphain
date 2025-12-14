from huggingface_hub import HfApi


def list_files():
    api = HfApi()
    dataset_id = "ColorSynth/GoMRI-17"
    print(f"Listing files in {dataset_id}...")
    files = api.list_repo_files(dataset_id, repo_type="dataset")
    for f in files[:10]:
        print(f)


if __name__ == "__main__":
    list_files()
