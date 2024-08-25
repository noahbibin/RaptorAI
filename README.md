<h1>Raptor AI: Hunt Down every detail</h1>
<img src="https://raw.githubusercontent.com/noahbibin/noahbibin.github.io/main/assets/RaptorAIsplashscreen.jpg" />
<p> Youth crime is quickly increasing, as well as robberies, knife crimes and murders. Some of these crimes take place under CCTV footage,
  but by the time security guards and the police find out, it's either to late or the damage is already done.
  We need a solution that can quickly detect a triggered item, or person, raising an alarm. Thats why I created Raptor AI.
</p>
<p>
  Raptor AI is an Object Detection AI powered by Pytorch and OpenCV. Raptor AI identifies objects as well as making an overlay on the footage from either a webcam or a IP camera, creating boxes over the detected items.
  Items that are in the list of Triggered Items result in raising an alarm. You can configure the settings for Raptor in the Configuration Window. These include the confidence threshold (Accuracy of detections),
  List of Triggered Items (Add or remove items that raise alarm), Change Alarm Sound (Choice of own sound), Camera Source (Webcam by default, as well as IP Camera Option), IP Camera URL (If IP camera is selected, default is used, can be changed).
</p>
<img src="https://raw.githubusercontent.com/noahbibin/noahbibin.github.io/main/assets/SydneyHarbourRaptor.png" />
<p>
  Looking at the image above, we can see an IP Camera Stream located in Sydney. I added boat in the list of Triggered Items. This results in all the boat getting a red outline and an alarm going off.
  Here is the Configuration Window for the image above.
</p>
<img src="https://raw.githubusercontent.com/noahbibin/noahbibin.github.io/main/assets/ConfigurationWindowSnapshot.png" />
