<h1>Raptor AI: Hunt Down every detail</h1>
<img src="https://raw.githubusercontent.com/noahbibin/noahbibin.github.io/main/assets/RaptorAIsplashscreen.jpg" />
<p>
Youth crime is rapidly rising, along with incidents of robbery, knife attacks, and murders. Although some of these crimes are captured on CCTV, it's often too late by the time security guards or the police are alerted—the damage has already been done. We need a solution that can swiftly detect a suspicious item or person and raise an alarm. That's why I created RAPTOR AI.
</p>
<p>

RAPTOR AI is a cutting-edge object detection system that leverages advanced AI technologies such as PyTorch and OpenCV in Python. It identifies objects, labels them, and draws bounding boxes around them in footage from either a webcam or an IP camera, highlighting the detected items. When an item from the Triggered Items list defined in Configuration is recognized, the system triggers an alarm and marks the item with a red box. This technology is designed to improve safety, wellbeing, and security across various locations, including community centers, schools, public areas, shopping centers, parks, and more.

</p>
<img src="https://raw.githubusercontent.com/noahbibin/noahbibin.github.io/main/assets/SydneyHarbourRaptorUpdated.png" />
<p>
 Looking at the image above, we can see an IP Camera stream from Sydney which is set to a public IP camera. I have added "person" to the list of Triggered Items, which results in person being highlighted with a red outline and triggering an alarm.
</p>

<p>
    You can configure RAPTOR AI's settings in the Configuration Window, which includes adjusting the confidence threshold (detection accuracy), managing the Triggered Items list (add or remove items that trigger an alarm), changing the alarm sound, selecting the camera source (webcam by default, with an IP camera option), and setting the IP camera URL (modifiable if IP camera is selected, with a default URL provided). The image below the Configuration Window for the Sydney Harbour detection shown in the image above.
</p>
<img src="https://raw.githubusercontent.com/noahbibin/noahbibin.github.io/main/assets/ConfigurationWindowSnapshotUpdated.png" />

<p>
This AI-powered software can help prevent fatal attacks and crimes, such as the Bondi Beach stabbings, by detecting the presence of knives and triggering an alert. This capability can save lives and enhance safety in schools and other locations, creating a safer environment overall.
</p>
<br/>
<h2>Prerequested to run the project</h2>
<p>
 <ol>
  <li>Install the latest version of python.</li>  
  <li>Install all dependencies:</li>
   <ul>
     <li>
  <code>pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118</code></li>
     <li>
  <code>pip install opencv-python pygame PyQt5</code></li>
    </ul>
   
 </ol>

</p>
