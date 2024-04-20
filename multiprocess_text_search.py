import multiprocessing
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

def worker(file_subset, keywords, output_queue):
    local_found = search_keywords_in_files(file_subset, keywords)
    output_queue.put(local_found)

def multiprocess_file_search(file_paths, keywords, num_processes=None):
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()

    split_files = [file_paths[i::num_processes] for i in range(num_processes)]
    output_queue = multiprocessing.Queue()
    processes = []

    for file_subset in split_files:
        process = multiprocessing.Process(target=worker, args=(file_subset, keywords, output_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    results = defaultdict(list)
    while not output_queue.empty():
        local_found = output_queue.get()
        for key, paths in local_found.items():
            results[key].extend(paths)

    return results

if __name__ == '__main__':
    file_paths = ["Text/file1.txt", "Text/file2.txt", "Text/file3.txt"]
    keywords = ["Тихий", "океану", "тайфуни", "риби",]
    
    start_time = time.time()
    multiprocess_results = multiprocess_file_search(file_paths, keywords)
    time_taken = time.time() - start_time
    print(f"Multiprocess search took {time_taken:.12f} seconds")
    print(multiprocess_results)

