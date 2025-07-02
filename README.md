<h3 align="center">ViSoND</h3>

  <p align="center">
    Visualizing and Sonifying Neural Data

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
    </li>
   <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#Converting neurophysiological data to MIDI">Converting neurophysiological data to MIDI</a></li>
        <li><a href="#Combining MIDI and video through VLC media player">Combining MIDI and video through VLC media player</a></li>
        <li><a href="#Combining MIDI with Video for more detailed examination through Ableton Live">Combining MIDI with Video for more detailed examination through Ableton Live (currently only functional for MacOS)</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

ViSoND is a tool designed to enhance observational investigation of simultaneously-acquired behavioral and neurophysiological data. This project follows in the footsteps of the original neurophysiologists, like Lord Adrian, who sonified neural data in order to observe neural activity. Here, we describe a simple method for converting neurophysiological data into MIDI files that can be listened to and examined alongside behavior recordings.

ViSoND allows for the discovery of patterns in data by human observation and provides a captivating method of data presentation.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

### Converting neurophysiological data to MIDI
The code in this [Google Colab notebook](https://colab.research.google.com/drive/1aRuu_-V5MDcN1ZE3Fvf4ls56Yp8eTmqK#scrollTo=gjTvZxUfF992) or the Jupyter Notebook in this repository walks through the process for converting any time series of discrete events into MIDI format. It also provides the option of uploading your own custom MIDI matrix.

For spiking data, you will simply need your data after spike-sorting with Kilosort and Phy.
For other data types, you will need to make an event file with 2 columns:
  * The first column specifies the variable that will be matched to a pitch. In spiking data, this would be the neuron identity. Examples of other variables are sniff frequency or gaze shifts
  * The second column has the event times

### Combining MIDI and video through VLC media player
The simplest way to combine MIDI with your video is through VLC, with an audio codec for MIDI files and and a SoundFont file.
  * Install [VLC](https://www.videolan.org/)
  * Make sure that your VLC installation has an audio codec that can process MIDI files
    * In VLC, go to Tools>Preferences
    * Choose the display mode called All (bottom left), then go to Input/Codecs > Audio codecs
    * If you see an audio codec called AUMIDI (Mac only) or Fluidsynth (any OS), proceed to next step. If you do not see one of these, install [fluidsynth](https://github.com/FluidSynth/fluidsynth/wiki/Download).
      * If you are on PC, you may need to first install [choclatey](https://chocolatey.org/install) via powershell (Run as admin)
  * Download any SoundFont file (.sf2). A popular choice is [FluidR3_GM](https://member.keymusician.com/Member/FluidR3_GM/index.html).
  * Upload that file to your audio codec.
    * Follow the same instructions listed above to access your audio codecs in VLC.
    * Select your MIDI codec (AUMIDI or Fluidsynth) and choose your SoundFont file. 


To play video with MIDI in VLC:
* Media>Open Multiple Files
* Add your video MP4 file
* Check box at bottom left for "Show More Options"
* Check "Play another media synchronously"
* Select your MIDI file
* Play!

### Combining MIDI with Video for more detailed examination through Ableton Live 
Install Ableton Live
* If you do not already have an Ableton Live license, then create an Ableton Live user account and purchase a license
* Follow [these instructions](https://help.ableton.com/hc/en-us/articles/209773565-Installing-Ableton-Live) to download Ableton Live
* Download the [Grand Piano Pack](https://www.ableton.com/en/packs/grand-piano/)

Running MIDI and Video in Ableton Live
* Open the ViSoND Ableton Live template with Ableton Live.
* Drag and drop your MIDI files and your video into the template at time 0.00.

  <img src="https://github.com/Smear-Lab/ViSoND/blob/main/Ableton_template.gif" width="700">
* Play!
* Navigation tools:
  * Move forward in time by dragging the time bar forward
* Extra capabilities and how to use them (*instructions, maybe a demo gif?*)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

(*License info?*)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

(*contact info*)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>
