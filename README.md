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
The code in this Google Colab notebook (link) or the Jupyter Notebook in this repository walks through the process for converting any time series of discrete events into MIDI format. It also provides the option of uploading your own custom MIDI matrix.

For spiking data, you will simply need your data after spike-sorting with Kilosort and Phy.
For other data types, you will need to make an event file with 2 columns:
  * The first column specifies the variable that will be matched to a pitch. In spiking data, this would be the neuron identity. Examples of other variables are sniff frequency or gaze shifts
  * The second column has the event times

### Combining MIDI and video through VLC media player
The simplest way to combine MIDI with your video is through VLC, with some added plug-ins.
  * Install [VLC](https://www.videolan.org/)
  * Install [choclatey](https://chocolatey.org/install) via powershell (Run as admin)
    * use choclatey to install [fluidsynth](https://github.com/FluidSynth/fluidsynth/wiki/Download)
      * Fluidsynth is audio codec needed to run midi files in VLC
      * Also download any SoundFont file (try searching for FluidR3_GM.sf2 online)
  * In VLC:
    * Tools>Preferences
    * Choose the display mode called All (bottom left), then go to Input/Codecs > Audio codecs > FluidSynth. Then select the .sf2 file with Browse button and save the preferences with Save button.

To play video with MIDI in VLC:
* Media>Open Multiple Files
* Add your video MP4 file
* Check box at bottom left for "Show More Options"
* Check "Play another media synchronously"
* Select your MIDI file
* Play!

### Combining MIDI with Video for more detailed examination through Ableton Live 
Install Ableton Live
* (*instructions for Ableton installation*)

Running MIDI and Video in Ableton Live
* (*instructions*)
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
