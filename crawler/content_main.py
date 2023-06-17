from helper import process_links
import pandas as pd

def main():
     # Replace with your actual URLs
    input_data=pd.read_csv("../processed_data/charter_links.csv")
    urls=list(input_data.url)
    contents = process_links(urls)

    # Create a DataFrame with URLs and their corresponding contents
    df = pd.DataFrame(contents, columns=['url', 'content'])
    df['content'] = df['content'].fillna('').apply(lambda x: x.encode('utf-8', 'ignore').decode('utf-8'))
    try: 
        df.to_csv("../processed_data/charter_contents.csv", escapechar='\\',index=False)
    except Exception as e:
            print(f"Error saving DataFrame to CSV: {e}")
            with open('output.txt', 'w') as f:
                for url, content in contents:
                    # Ensure content is not None and remove any newline characters
                    if content is not None:
                        content = content.replace('\n', ' ').replace('\r', '')
                    f.write(f"{url}\t{content}\n")

if __name__ == "__main__":
    main()
