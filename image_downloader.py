# -*- coding: utf-8 -*-
# author: Yabin Zheng
# Email: sczhengyabin@hotmail.com

from __future__ import print_function

import argparse
import os
import crawler
import downloader
import sys


def main(argv):
    parser = argparse.ArgumentParser(description="Image Downloader")
    parser.add_argument("--keywords", type=str,
                        help='Keywords to search. ("in quotes")')
    parser.add_argument("--engine", "-e", type=str, default="Bing",
                        help="Image search engine.", choices=["Google", "Bing", "Baidu"])
    parser.add_argument("--driver", "-d", type=str, default="chrome_headless",
                        help="Image search engine.", choices=["chrome_headless", "chrome", "phantomjs"])
    parser.add_argument("--max_number", "-n", type=int, default=10,
                        help="Max number of images download for the keywords.")
    parser.add_argument("--num-threads", "-j", type=int, default=50,
                        help="Number of threads to concurrently download images.")
    parser.add_argument("--timeout", "-t", type=int, default=20,
                        help="Seconds to timeout when download an image.")
    parser.add_argument("--output", "-o", type=str, default="./download_images",
                        help="Output directory to save downloaded images.")

    ### Edge specific options                        
    parser.add_argument("--safe_mode", "-S", action="store_true", default=False,help="Turn on safe search mode")
    
    parser.add_argument("--color", "-cl", type=str, default=None,help="Specify the color of desired images.")

    parser.add_argument("--type", "-ty", type=str, default=None,help="What kinds of images to download.",
    choices=["clipart", "line_drawing", "photograph","animated_gif","transparent"])    
    
    parser.add_argument("--size", default=None,help="Specify the image size",
    choices=["small","medium","large","extra_large","custom"])
    
    parser.add_argument("--layout", default=None,help="Specify the image layout",
    choices=["square","wide","tall",])
    
    parser.add_argument("--photo", default=None,help="Specify the photo type",
    choices=["face","body"])
    
    parser.add_argument("--date", default=None,help="Specify the image date",
    choices=["past_day","past_week","past_month","past_year"])

    parser.add_argument("--width", type=int,default=None,help="Specify the image width")
    
    parser.add_argument("--height", type=int,default=None,help="Specify the image height")
    
    args = parser.parse_args(args=argv)
    
    if args.size == 'custom' and (args.width == None or args.height == None):
        print('Height and Width cannot be None when the image size is set to custom')
        return
    
    elif args.size != 'custom' and (args.width != None or args.height != None):
        print('Height and Width cannot be specified when the image size is not set to custom')
        return

    print('Crawling the urls.....')
    
    crawled_urls = crawler.crawl_image_urls(args.keywords,engine=args.engine,
                                            max_number=args.max_number,browser=args.driver,
                                            safe_mode=args.safe_mode,quiet=False,
                                            color = args.color, image_type = args.type, 
                                            size = args.size, layout = args.layout, 
                                            photo = args.photo, date = args.date, 
                                            width = args.width, height = args.height)
    
    downloader.download_images(image_urls=crawled_urls, max_number=args.max_number,
                               dst_dir= os.path.join(args.output,args.keywords),
                               concurrency=args.num_threads, timeout=args.timeout,
                               file_prefix=args.engine)

    print("Finished.")


if __name__ == '__main__':
    main(sys.argv[1:])
