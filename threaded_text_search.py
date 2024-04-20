import threading
from collections import defaultdict
import time

def search_keywords_in_files(file_list, keywords):
    found = defaultdict(list)
    for file_path in file_list:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            for keyword in keywords:
                if keyword in content:
                    found[keyword].append(file_path)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    return found

def threaded_file_search(file_paths, keywords, num_threads=4):
    split_files = [file_paths[i::num_threads] for i in range(num_threads)]
    results = defaultdict(list)
    threads = []
    result_lock = threading.Lock()
    
    def worker(file_subset):
        local_found = search_keywords_in_files(file_subset, keywords)
        with result_lock:
            for key, paths in local_found.items():
                results[key].extend(paths)

    for file_subset in split_files:
        thread = threading.Thread(target=worker, args=(file_subset,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return results

if __name__ == '__main__':
    file_paths = ["Text/file1.txt", "Text/file2.txt", "Text/file3.txt"] 
    keywords = ["Тихий", "океану", "тайфуни", "риби",]
    
    start_time = time.time()
    threaded_results = threaded_file_search(file_paths, keywords, num_threads=3)
    time_taken = time.time() - start_time
    print(f"Threaded search took {time_taken:.12f} seconds")
    print(threaded_results)




