#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include <iostream>
#include "ros/ros.h"
#include <sensor_msgs/PointCloud2.h>
#include <geometry_msgs/Point.h>

using namespace std;
void pixelTo3DPoint(const sensor_msgs::PointCloud2 pCloud, const int u, const int v, geometry_msgs::Point &p , int i )
{
  // get width and height of 2D point cloud data
  int width = pCloud.width;
  int height = pCloud.height;
  //ROS_INFO("%s", msg.data.c_str());


  // Convert from u (column / width), v (row/height) to position in array
  // where X,Y,Z data starts
  int arrayPosition = v*pCloud.row_step + u*pCloud.point_step;

  // compute position in array where x,y,z data start
  int arrayPosX = arrayPosition + pCloud.fields[0].offset; // X has an offset of 0
  int arrayPosY = arrayPosition + pCloud.fields[1].offset; // Y has an offset of 4
  int arrayPosZ = arrayPosition + pCloud.fields[2].offset; // Z has an offset of 8

  float X = 0.0;
  float Y = 0.0;
  float Z = 0.0;
 
  memcpy(&X, &pCloud.data[arrayPosX], sizeof(float));
  memcpy(&Y, &pCloud.data[arrayPosY], sizeof(float));
  memcpy(&Z, &pCloud.data[arrayPosZ], sizeof(float));
  if( i==0){
  cout<< "X1: "<< X <<endl;
  cout<< "Y1: "<< Y <<endl;
  cout<< "Z1: "<< Z <<endl; 
  }
  else if(i==1){
  cout<< "X2: "<< X <<endl;
  cout<< "Y2: "<< Y <<endl;
  cout<< "Z2: "<< Z <<endl; 
  }
 else if(i==2){
  cout<< "X3: "<< X <<endl;
  cout<< "Y3: "<< Y <<endl;
  cout<< "Z3: "<< Z <<endl; 
		}
 else if(i==3){
  cout<< "X4: "<< X <<endl;
  cout<< "Y4: "<< Y <<endl;
  cout<< "Z4s: "<< Z <<endl; 
		}
  
  p.x = X;
  p.y = Y;
  p.z = Z;

}
void callback(const sensor_msgs::PointCloud2::ConstPtr&);

geometry_msgs::Point P;

int main(int argc, char **argv)
{

	ros::init(argc, argv, "Pub_Sub");

	ros::NodeHandle n;
	std::string topic = n.resolveName("/camera/depth/points");
	uint32_t queue_size = 100;	

	ros::Subscriber sub = n.subscribe<sensor_msgs::PointCloud2> (topic, queue_size, callback);
	
	ros::Publisher pose_pub = n.advertise<geometry_msgs::Point>("pose", 100);
	
    ros::Rate r(10);
	ros::spinOnce();
	
  
	while(n.ok()){
    
    ros::Time scan_time = ros::Time::now();
	pose_pub.publish(P);
	
	ros::spinOnce();

    r.sleep();
  }

	return 0;
}


void callback(const sensor_msgs::PointCloud2::ConstPtr& pc)
{	int i, u, v;
	for(i=0;i<4;i++){
		if( i==0){
			u = 344;
			v = 51;
		}
		else if(i==1){
			u = 298;
			v = 79;
		}
		else if(i==2){
			u = 396;
			v = 78;
		}
		else if(i==3){
			u = 344;
			v = 123;
		}
	pixelTo3DPoint(*pc,u,v,P,i);
	}
	
}
//[ WARN] [1536649569.066546033]: Camera calibration file /home/kartik/.ros/camera_info/depth_Astra_Orbbec.yaml not found.



