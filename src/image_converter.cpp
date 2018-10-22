#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include <iostream>
#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <cv_bridge/cv_bridge.h>


static const std::string OPENCV_WINDOW = "Image window";
static const std::string OPENCV_WINDOW2 = "Image windowrgb";

namespace enc = sensor_msgs::image_encodings;

class ImageConverter
{
  ros::NodeHandle nh_;
  image_transport::ImageTransport it_;
  image_transport::Subscriber image_sub_;
  image_transport::Subscriber rgbimage_sub_;

  image_transport::Publisher image_pub_;

public:
  ImageConverter()
    : it_(nh_)
  {
    // Subscrive to input video feed and publish output video feed
    image_sub_ = it_.subscribe("/camera/depth/image", 1,
      &ImageConverter::imageCb, this);
    rgbimage_sub_ = it_.subscribe("/camera/rgb/image_raw", 1,
      &ImageConverter::rgbimageCb, this);
    image_pub_ = it_.advertise("/image_converter/output_video", 1);

    cv::namedWindow(OPENCV_WINDOW);
    cv::namedWindow(OPENCV_WINDOW2);


  }

  ~ImageConverter()
  {
    cv::destroyWindow(OPENCV_WINDOW);
  }

void imageCb(const sensor_msgs::ImageConstPtr& msg)
{
  cv_bridge::CvImageConstPtr cv_ptr;
  try
  {
    if (enc::isColor(msg->encoding))
      cv_ptr = cv_bridge::toCvShare(msg, enc::BGR8);
    else
      cv_ptr = cv_bridge::toCvShare(msg, enc::TYPE_32FC1);
  }
  catch (cv_bridge::Exception& e)
  {
    ROS_ERROR("cv_bridge exception: %s", e.what());
    return;
  }
  cv::Mat dst;
  //cv_ptr->image.convertTo(dst,CV_8UC1, 255.0);
  cv::normalize(cv_ptr->image, dst, 0, 255, cv::NORM_MINMAX, CV_8UC1);
  cv::imshow(OPENCV_WINDOW, dst);
  cv::imwrite("/home/kartik/stair_depth_data/stairdepth3.jpg", dst);

  cv::waitKey(3);
}

void rgbimageCb(const sensor_msgs::ImageConstPtr& msg)
{
  cv_bridge::CvImageConstPtr cv_ptr;
  try
  {
    if (enc::isColor(msg->encoding))
      cv_ptr = cv_bridge::toCvShare(msg, enc::BGR8);
    else
      cv_ptr = cv_bridge::toCvShare(msg, enc::TYPE_32FC1);
  }
  catch (cv_bridge::Exception& e)
  {
    ROS_ERROR("cv_bridge exception: %s", e.what());
    return;
  }
  cv::Mat dst;
  //cv_ptr->image.convertTo(dst,CV_8UC1, 255.0);
  cv::imshow(OPENCV_WINDOW2, cv_ptr->image);
  cv::imwrite("/home/kartik/stair_depth_data/stairRGB3.jpg", cv_ptr->image);
  cv::waitKey(3);
}
};

int main(int argc, char** argv)
{
  ros::init(argc, argv, "image_converter");
  ImageConverter ic;
  ros::spin();
  return 0;
}
