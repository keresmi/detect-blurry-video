#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import argparse
import sys
import cv2
from detect_blurry_image import detect_blurry_image

def detect_blurry(video_path, results_path, threshold, min_zero, frame_interval):
    print 'Video:', video_path

    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print "Error, could not open the video", video_name
        sys.exit(1)

    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(video.get(cv2.CAP_PROP_FPS))
    pos_frame = 0
    number_of_blur = 0

    file = open(results_path, 'wb')
    file.write('Timestamp, Per, Blur extent, Blurred')
    file.write('\n')

    print 'Total frames: ', total_frames
    print 'FPS: ',fps
    print 'Duration: ', (total_frames / fps),'s'

    while pos_frame < total_frames:
        video.set(cv2.CAP_PROP_POS_FRAMES, pos_frame)
        flag, img = video.read()
        timestamp = video.get(cv2.CAP_PROP_POS_MSEC)

        # gray is good for image processing
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        per, blur_extent, blurred = detect_blurry_image(gray, threshold, min_zero)

        file.write('{0}, {1}, {2}, {3}'.format(timestamp, per, blur_extent, blurred))
        file.write('\n')
        print 'Timestamp: {0}, per: {1}, blur extent: {2}, blurred: {3}'.format(timestamp, per, blur_extent, blurred)

        if blurred:
            number_of_blur += 1

        pos_frame += frame_interval

    video.release()
    file.close

    if number_of_blur >= (total_frames/frame_interval*0.5):
        print 'A blurry video'
    else:
        print 'Not a blurry video'


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Blur detection for video')
    parser.add_argument('-i', '--input_path', dest='input_path', type=str, required=True, help="video path")
    parser.add_argument('-o', '--output_path', dest='output_path', type=str, required=True, help="path to save results")
    # parameters
    parser.add_argument("-t", "--threshold", dest='threshold', type=int, default=35, help="threshold parameter")
    parser.add_argument("-m", "--min_zero", dest='min_zero', type=float, default=0.025, help="min zero parameter")
    parser.add_argument("-f", "--frame_interval", dest='frame_interval', type=int, default=1, help="frame interval parameter")

    args = parser.parse_args()
    detect_blurry(args.input_path, args.output_path, args.threshold, args.min_zero, args.frame_interval)
