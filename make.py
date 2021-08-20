#!/usr/bin/env python3
# coding: utf-8

import dominate
import markdown2
import shutil
import os
import sys
import json

def build_file(path, doc):
    dirpath = os.path.join("docs", os.path.dirname(path))
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    f = open(os.path.join("docs", path), "w")
    f.write(str(doc))
    f.close()

def convert_line(line):
	if (line.startswith("//sticker")):
		line = line[10:]
		dct = json.loads(line)
		line = f' <a href="{dct["img"]}"><img src="{dct["img"]}" style="width:300px;"/></a>'
		return line

	return line

def page_generate(path, title, mdpath):
	lines = open(mdpath).readlines()

	for i in range(len(lines)):
		lines[i] = convert_line(lines[i])

	text = "\n".join(lines)

	page = dominate.document(title=title)
	with page:
		dominate.tags.meta(charset=u"utf-8")

	header = page.add(dominate.tags.div(id="header", cls="header"))
	content = page.add(dominate.tags.div(id="content"))
	footer = page.add(dominate.tags.div(id="footer"))

	nav = content.add(dominate.tags.nav(cls="nav"))
	article = content.add(dominate.tags.article(cls="article"))

	with page.head:
		dominate.tags.link(rel="stylesheet", href="main.css")

	with header:
		with dominate.tags.h1():
			dominate.tags.a("Выхухоль и Ко", href="index.html", cls="header_ref")

		dominate.tags.a("Главная", href="index.html")
		dominate.tags.a("Мироскоп", href="enchantment.html")
		dominate.tags.a("Бестиарий", href="creatures.html")
		dominate.tags.a("Артефакты", href="artefacts.html")

	with article:
		dominate.util.raw(
			markdown2.markdown(text, extras=[
							   "fenced-code-blocks", "tables", "header-ids"])
		)

	build_file(path, page)


# Подготавка файлов русской версии.
for f in os.listdir("text"):
	target = os.path.splitext(f)[0] + ".html"
	page_generate(
		path=target,
		title="MuskratAndCompany",
		mdpath=os.path.join("text", f)
	)

shutil.copytree("images", "docs/images", dirs_exist_ok=True)
shutil.copyfile("main.css", "docs/main.css")

os.system("./archive.sh")