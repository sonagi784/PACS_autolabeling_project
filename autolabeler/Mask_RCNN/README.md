logs 폴더에 mask_rcnn_object_0010.h5 넣어주시고,

Maks_RCNN 폴더에 mask_rcnn_coco.h5 넣어주세요



Mask_RCNN/mrcnn/visualize.py
![visualize 변경](https://user-images.githubusercontent.com/75662287/119297250-902dc600-bc95-11eb-8b7a-6bdc4d837e48.PNG)


app.py

![app rootdir 변경](https://user-images.githubusercontent.com/75662287/119297269-96bc3d80-bc95-11eb-96b4-1bd7ab1a3c57.PNG)
![app 추가dir 변경](https://user-images.githubusercontent.com/75662287/119297276-98860100-bc95-11eb-90bc-5d71c849f461.PNG)

위 두개 파일들 경로변경하시고 app.py 실행하시면 됩니다.

!pip install gevent <- 해주셔야합니다.

----
!pip install tensorboard==1.15.0 tensorflow==1.15.0 tensorflow-estimator==1.15.1 tensorflow-gpu==1.15.2 tensorflow-gpu-estimator==2.1.0 Keras==2.2.5 Keras-Applications==1.0.8 Keras-Preprocessing==1.1.0

mask rcnn 실행하려면 tensorflow 버전을 낮춰야해서 위에 버전으로 설정하시면 됩니다.





