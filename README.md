# 平板套装科技广告 Skill

支持 TAB9、P30、P60、P80、P90、T10、T901、TAB10、TB02、S80、S90，附各型号机身原图与公共配件。

每次生成四段各 10 秒视频所需的宫格参考图、对应 Gemini 完整提示词和一张简表。整片包含强运动、速度变化，以及多处科技概念与真实平板的联系。美工将图和提示词交给 Gemini 网页端，再裁剪拼接视频。

## 克隆与使用

~~~bash
git clone https://github.com/Neewi/tablet-tech-ad-storyboard.git
~~~

在支持图片生成的 Codex 中打开克隆后的文件夹，新建聊天，发送下面这段请求。项目说明会引导 Codex 读取根目录的 SKILL.md。

> 请读取当前项目的 SKILL.md 并按其流程执行，为 TAB9 制作四段广告素材。参数不上屏，包含充电头。

也可以指定其他支持型号。需要明确三个信息。

- 产品型号。
- 参数是否直接生成进视频画面。
- 是否包含充电头。本项目套装约定亚马逊包含、Temu 不包含，以实际售卖版本为准。

参数不上屏时可以直接制作。参数上屏时，需要补齐本次实际配置，Codex 会集中询问缺项。

使用内置图片生成工具，所用 Codex 需要具备该工具及可用额度。素材路径已打包，无需本项目创建者电脑上的原始目录。

## 获取结果

成品位于项目内 `outputs/<型号>/<本次运行目录>/`，每次包含四张宫格、四条提示词和 `对应表.md`。过程资料位于 `work/<本次运行目录>/`。

两个目录均已被 Git 忽略。原始产品素材保存在 `assets/` 并随仓库版本管理。图片中的参考编号用于说明关键帧，最终视频按正常全屏画面生成。

## 更新

在 Codex 中打开同一个克隆目录，运行 `git pull --ff-only` 获取更新，然后新建聊天使用。若此前另行复制到个人 skills 目录，应同步更新该副本，避免调用旧版。

修改 skill 后，在仓库根目录检查和推送。

~~~bash
git status --short
git add SKILL.md references assets scripts agents AGENTS.md README.md .gitignore requirements.txt
git commit -m "Update tablet ad skill"
git push
~~~

输出和过程目录会被忽略。不要使用 `git add -f` 强制提交生成结果。单次工作记录仅用于本次返修。

## 素材完整性检查

检查脚本需要 Python 3.9 及以上与 Pillow。

~~~bash
python3 -m pip install -r requirements.txt
python3 scripts/check-assets.py --model TAB9
~~~

脚本检查引用、哈希和图片可读取性。宫格中的外观、人物视线和实体概念联系仍需 Codex 实际查看审核。Gemini 视频生成后，还需检查动态外观和运动执行。
