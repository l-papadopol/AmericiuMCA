<!DOCTYPE html>
<html lang="en">
  <head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <meta name="author" content="Papadopol Lucian Ioan">
  </head>
  <body>
    <h1 style="text-align: center;"><span style="color: #000099;"><b>AmericiuMCA</b></span></h1>
    <div style="text-align: center;"><img src="7%25%20crystal.png"
        alt="s" title="a" style="width: 602px; height: 304px;"></div>
    <h4><span style="color: #006600;">DESCRIPTION</span></h4>
    <p>AmericiuMCA is a software that implements multi-channel analyzer
      functionality for gamma ray spectroscopy purposes.</p>
    <p>Its main goal is providing to the user the possibility to use different
      hardware for pulse acquisition and have a single, fast </p>
    <p>software MCA. </p>
    <p>At this current development stage, it disclose the power of the Canberra
      556AIM NIM ADC to Ethernet acquisition module via EPICS + MCA package
      connectivity.</p>
    <h4><span style="color: #006600;">REQUIREMENTS</span></h4>
    <p>It's required to have a NIM BIN system set up for gamma spectroscopy with
      Camberra 556AIM module.</p>
    <p>The 556AIM is accessed by EPICS package via mca module. It's mandatory to
      have EPICS + mca module correctly installed and configured.</p>
    <p>You can find here a complete guide to how to do that. <a href="http://www.nuclearphysicslab.com/npl/npl-home/spectroscopy/software_and_hardware/diy-canberra-system/">Nuclear
        Physiscs Lab - Amateur Canberra Spectroscopy</a></p>
    <h4><span style="color: #006600;">SOFTWARE REQUIREMENTS</span></h4>
    <p>AmericiuMCA is written in python and uses various extensions. You need to
      have installed python interpreter and the following extensions:</p>
    <ul>
      <li>pygame</li>
      <li>numpy</li>
      <li>matplotlib</li>
      <li>pyepics</li>
    </ul>
    <p>Installation of this extensions is straightforward using "pip":</p>
    <ul>
      <li>
          <meta http-equiv="content-type" content="text/html; charset=utf-8">
          <tt>pip install pyepics pygame numpy matplotlib</tt></li>
    </ul>
    <h4><span style="color: #006600;">HOW TO EXECUTE<br>
      </span></h4>
    <p>After downloading the latest version from GitHub repository, unpack it
      in.</p>
    <p>To put in execution the software, use your command line shell, move in to
      the folder where you have unpacked it and execute by typing </p>
    <ul>
      <li><tt><tt>python main.py</tt></tt></li>
    </ul>
    <h4><span style="color: #006600;">INTERFACE</span></h4>
    <p>The user interface is minimalist and takes advantage of it to speed up
      the operation of the software.</p>
    <p>Commands are typed directly by keyboard without the need of any clicking
      around.</p>
    <p>Mouse wheel is used to move main vertical red cursor by one channel
      increment/decrements.</p>
    <p>Keyboard arrows left and right are used for the same porpoise but with
      ten channel increment/decrements.</p>
    <p><h5><span style="color: #006600;">COMMANDS</span></h5></p>
    <ul>
      <li>start&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; starts the acquisition&nbsp;
        but prior it resets/cancels the previously acquired spectra / 556AIM
        memory</li>
      <li>stop &nbsp; &nbsp; &nbsp;&nbsp; stops the acquisition</li>
      <li>resume&nbsp;&nbsp; resume the acquisition without altering previously
        acquired spectra / 556AIM memory</li>
      <li>plt&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; plot
        the linearity chart</li>
      <li>plot&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; plot the
        calibrated spectra</li>
       <li>printraw&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; print as *.pdf the raw
       spectra data</li>
    </ul>
    <p><h5><span style="color: #006600;">SHORTCUTS</span></h5></p>
    <ul>
      <li>Ctrl + a&nbsp;&nbsp;&nbsp; set calibration marker A on channel
        selected by main cursor</li>
      <li>Ctrl + b&nbsp;&nbsp;&nbsp; set calibration marker B on channel
        selected by main cursor</li>
      <li>Ctrl + c&nbsp;&nbsp;&nbsp; set calibration marker C on channel
        selected by main cursor</li>
      <li>Ctrl + x&nbsp;&nbsp;&nbsp; cancel peak selection markers</li>
      <li>Ctrl + j&nbsp;&nbsp;&nbsp; cancel calibration points A, B, C markers</li>
      <li>Ctrl + l&nbsp;&nbsp;&nbsp; set left peak skirt point for peak
        selection</li>
      <li>Ctrl + r&nbsp;&nbsp;&nbsp; set right peak skirt point for peak
        selection</li>
    </ul>
    <p><h5><span style="color: #006600;">LIN/LOG SCALE</span></h5></p>
    The main window alias "working window", have as per default linear scale.<br>
    All the operations, calibration, FWHM measure etc... are performed in this window.<br>
    The logarithmic scale is only available after energy calibration on the secondary windows "Calibrated spectra" that is called
    with the command "plot"<br>
    <div style="text-align: center;"><img src="avoid_colours.png"
        alt="s" title="a" style="width: 602px; height: 304px;"></div>
    This is standard linear scale of the plot shown after issuing the command "plot".<br>
    Clicking on the button on the top right you can switch to logarithmic scale.<br>
    <div style="text-align: center;"><img src="avoid_colours_2.png"
        alt="s" title="a" style="width: 602px; height: 304px;"></div>
        <br>
    <p><h5><span style="color: #006600;">ENERGY CALIBRATION</span></h5></p>
    AmericiuMCA have implemented quadratic fitting energy calibration. To calibrate a spectra you need to clearly recognize three isotope peaks and
    already know their energy.<br>
    Use the keyboard arrows or mouse wheel to select first, lowest energy isotope peak tip. Type the energy in keV without pressing "Enter",
    press Ctrl + a. A purple calibration marker labelled "A" will appear. Continue with the middle energy peak and Ctrl + B then for the highest enery peak and Ctrl + C. <br>
    Now that you have set the three calibration points, you can show the linearity of your probe plot by typing command "plt".<br>
    To show energy calibrated spectra issue the command "plot".<br>
    The shortcut Ctrl + j resets the three calibration points.<br><br>
    <div style="text-align: center;"><img src="colored.png"
        alt="s" title="a" style="width: 602px; height: 304px;"></div>
    <h4><b><span style="color: #006600;">LICENCE</span><br>
      </b></h4>
    <pre><meta http-equiv="content-type" content="text/html; charset=utf-8"><pre>Copyright (c) 2023, Papadopol Lucian Ioan
All rights reserved. Contact: l.i.papadopol "@" gmail.com

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. All advertising materials mentioning features or use of this software
   must display the following acknowledgement:
   This product includes software developed by the &lt;organization&gt;.
4. Neither the name AmericiuMCA / Papadopol Lucian Ioan / Madexp nor the
   names of its contributors may be used to endorse or promote products
   derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY PAPADOPOL LUCIAN IOAN ''AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL PAPADOPOL LUCIAN IOAN BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.</pre></pre>
  </body>
</html>
