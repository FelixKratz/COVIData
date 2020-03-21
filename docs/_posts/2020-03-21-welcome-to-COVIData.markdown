---
layout: post
title:  "Herzlich Willkommen!"
date:   2020-03-21 14:04:03 +0100
categories: graphics demo 
---

Herzlichen Willkommen auf unserer kleinen
[github-page](https://pages.github.com/).
Auf dieser Seite veröffentlichen wir 
Informationen zu unserem kleinen
Projekt beim [wirvsvirus](https://wirvsvirushackathon.org/) Hackathon.

<p><a href="https://commons.wikimedia.org/wiki/File:SEIR.PNG#/media/File:SEIR.PNG"><img src="https://upload.wikimedia.org/wikipedia/commons/3/3d/SEIR.PNG" alt="SEIR compartmental model" width="640" height="71"></a><a href="https://commons.wikimedia.org/w/index.php?curid=12885405">Link</a></p>

Erste kleine Ziele sind die Verknüpfung der
Daten der [John-Hopkins-Universität](https://github.com/CSSEGISandData/COVID-19)
für die Ausbreitung von COVID-19 weltweit, mit einem
[SEIR-Model](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SEIR_model),
welches mit dem [Euler-Verfahren](https://de.wikipedia.org/wiki/Explizites_Euler-Verfahren) gelöst
wird. 
<p>
<a href="https://commons.wikimedia.org/wiki/File:Euler_method.svg#/media/File:Euler_method.svg">
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Euler_method.svg/307px-Euler_method.svg.png" alt="Euler method.svg">
</a>
<br>Public Domain, 
<a href="https://commons.wikimedia.org/w/index.php?curid=2143753">Link</a>
</p>

Die Daten sollen dabei auf dieser
Seite veröffentlicht werden und die Modelparameter
evtl. interaktiv darüber steuerbar sein. Weitergehend
könnte es interessant sein andere verfügbare [Daten](https://docs.google.com/spreadsheets/d/13la9BFcPUeZKnx6amfwogzmhcNxtF_ouBiV6aOpDHFM/edit#gid=0)
mit einzubeziehen. 

So kann man dann interaktiv austesten, was "flatten the curve"
aktuell in Deutschland bedeutet.

<a title="Siouxsie Wiles and Toby Morris / CC BY-SA (https://creativecommons.org/licenses/by-sa/4.0)"
    href="https://commons.wikimedia.org/wiki/File:Covid-19-curves-graphic-social-v3.gif">
    <img width="512"
    alt="Covid-19-curves-graphic-social-v3"
    src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Covid-19-curves-graphic-social-v3.gif/512px-Covid-19-curves-graphic-social-v3.gif">
</a>

Die Idee des Projekts basiert vorallem auf der Darstellung der 
JHU-Daten nach [Paul Em](https://paul-em.github.io/covid-19-curves/)
und dem interaktiven [Epidemic Calculator](https://gabgoh.github.io/COVID/index.html).

Dafür wirken an diesem Projekt aktuell folgende Leute mit:

<ul>
{% for member in site.data.members %}
  <li>
    <a href="https://github.com/{{ member.github }}">
      {{ member.name }}
    </a>
  </li>
{% endfor %}
</ul>

