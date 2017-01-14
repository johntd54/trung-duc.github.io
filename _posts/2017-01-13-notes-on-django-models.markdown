---
layout: post
title: "170113 - Notes on Django Models"
date: 2017-01-13 16:45:27
categories: django
---

In case that you want to modify `ManyToManyField`, the best bet is to:

1. Create a backup of the the field's through table
2. Delete the ManyToManyField, and migrate this change to the database. This will drop the `ManyToManyField` from the database, and will also drop the through table inside the database (if you use default through table)
3. Add back ManyToManyField inside your model, with your desired options, and migrate it back to the database.

