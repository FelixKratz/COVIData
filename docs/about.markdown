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