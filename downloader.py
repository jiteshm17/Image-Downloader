""" Download image according to given urls and automatically rename them in order. """
# -*- coding: utf-8 -*-
# author: Yabin Zheng
# Email: sczhengyabin@hotmail.com

from __future__ import print_function

import os
import concurrent.futures
import requests

success_count = 0

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Proxy-Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, sdch",
    # 'Connection': 'close',
}

processed_urls = set()

def download_image(image_url, dst_dir, file_name, timeout=20):
    global success_count
    while True:
        try:
            response = requests.get(
                image_url, headers=headers, timeout=timeout)
            response.close()
            if response.status_code == 200:
                new_file_name = "{}.{}".format(file_name, "jpg")
                new_file_path = os.path.join(dst_dir, new_file_name)
                with open(new_file_path, 'wb') as f:
                    f.write(response.content)
                
                success_count += 1
                # print("## OK:  {}  {}".format(new_file_name, image_url))
            else:
                print("## Err:  {}".format(image_url))
            break
        except Exception as e:
            print("## Fail:  {}  {}".format(image_url, e.args))
            break


def download_images(image_urls, max_number,dst_dir, file_prefix="img", concurrency=50, timeout=20):
    """
    Download image according to given urls and automatically rename them in order.
    :param timeout:
    :param image_urls: list of image urls
    :param dst_dir: output the downloaded images to dst_dir
    :param file_prefix: if set to "img", files will be in format "img_xxx.jpg"
    :param concurrency: number of requests process simultaneously
    :return: none
    """
    all_image_urls = set(image_urls)
    processed_urls = set()
    count = 0
    global success_count

    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        future_list = list()
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for image_url in image_urls[:max_number]:
            file_name = file_prefix + "_" + "%04d" % count
            processed_urls.add(image_url)
            future_list.append(executor.submit(
                download_image, image_url, dst_dir, file_name, timeout))
            
            count += 1
        concurrent.futures.wait(future_list, timeout=180)

    remaining_count = max_number - success_count
    remaining_urls = all_image_urls.difference(processed_urls)
    
    print('Processing remaining {} images'.format(remaining_count))
    for image_url in remaining_urls:
        file_name = file_prefix + "_" + "%04d" % count
        download_image(image_url, dst_dir, file_name, timeout)
        if success_count == max_number:
            print('Downloaded {} images'.format(max_number))
            break
        count += 1


