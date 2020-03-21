---
layout: page
title: About
permalink: /about/
---

Wir sind ein kleines Team aus Deutschland, die
an dem [wirvsvirus](https://wirvsvirushackathon.org/) hackathon teilnehmen.
Unser code befindet sich auf [github](https://github.com/FelixKratz/COVIData).

We're a small team from Germany contributing
to the [wirvsvirus](https://wirvsvirushackathon.org/) hackathon.
Our code is hosted at [github](https://github.com/FelixKratz/COVIData).

Mitwirkende/ Contributors:

<ul>
{% for member in site.data.members %}
  <li>
    <a href="https://github.com/{{ member.github }}">
      {{ member.name }}
    </a>
  </li>
{% endfor %}
</ul>

Was "flatten the curve" bedeutet ist in folgendem Comic ganz gut dargestellt (aus der 
englischen [Wikipedia](https://en.wikipedia.org/wiki/Coronavirus_disease_2019) zu COVID19).

<a title="Siouxsie Wiles and Toby Morris / CC BY-SA (https://creativecommons.org/licenses/by-sa/4.0)"
    href="https://commons.wikimedia.org/wiki/File:Covid-19-curves-graphic-social-v3.gif">
    <img width="512"
    alt="Covid-19-curves-graphic-social-v3"
    src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Covid-19-curves-graphic-social-v3.gif/512px-Covid-19-curves-graphic-social-v3.gif">
</a>