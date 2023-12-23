# ImageBase64

## 编写目的

这个脚本是为了使我在使用 `Marksown` 编写内容时, 更好的添加图片.
我一般是用[Base64的方式](#Markdown通过Base64添加图片)来在 `.md` 文件中添加图片, 你可能会问我 `为什么不使用图床?`, 我的回答是 `我保证数据的完整`
如果图床失效了, 那就会影响文档的阅读, 所以我一般选择本地存储.
然而我之前把图片存在 `.md` 的同一级目录下, 但是这样子会导致一篇文章的文件数量过多
所以我在了解Base64的方法加图片后, 我果断选择了这个方法
但是在图片转Base64又是一个麻烦的地方, 比如在线网站不能批量转换, 不支持 `.webp`、`.avif` 的格式
于是就诞生了写这个脚本的念头

## 配置文件介绍

为了使这个脚本更加有可调节性, 我采用了配置文件的方式进行调控参数

配置文件如下:

``` ini
[ImageToBase64]
; 是否添加markdoown语法
addmarkdown = True
allinone = True
allinonefile = allinone.txt

[ImageToIamge]
defaultformat = webp

[Base64ToImage]
; base64中是否含有markdown语法
withmarkdown = True
```

`ImageToBase64`, `ImageToIamge`, `Base64ToImage` 分别对应着
`图片转Base64模块`, `图片转图片模块`, `Base64转图片模块` 的配置

### 在 `ImageToBase64` 中

#### addmarkdown

`addmarkdown` 指的是是否添加Markdown语法

True和False分别为如下效果(Base64的编码省略了一部分)

True
```
[testImage]:data:image/avif;base64,AAAAIGZ0eXBhd...
```
`[testImage]:data:image/avif;base64,` 这一段就是Markdown语法, 看下文的直观解释

[ `图片名(由被转码的图片提供)` ]:data:image/ `图片的格式(由程序通过文件名后缀自动识别)` ;base64,

False
```
AAAAIGZ0eXBhd...
```

#### allinone & allinonefile

这两个应该放在一起说, 就是让用户决定是否将转码的Base64编码放在一个文件中
`allinone` 如果是 `True` 就是会生成一个 `allinonefile` 为名的文件存放所有的Base64编码, 反之则不会

**注意: 每次启动程序都会删除原本存在 `allinonefile` 这个文件**

目前还有个问题, 就是生成的 `allinonefile` 只会保存在exe的同级目录下, 并且如果程序传入多个文件夹路径, 会将它们的Base64编码保存在同一 `allinonefile` 中, 这明显不是我想要的结果

### 在 `ImageToIamge` 中

#### defaultformat

这个参数指的是图片转图片的默认格式

为了使我的 `.md` 文件不会过大, 所以我会采用 `.webp`, `.avif` 的格式, 先将其他图片格式进行转换
因为有些地方并不支持 `.avif`, 所以我就加了这个参数
方便我调节其他图片格式转换成的格式

### `Base64ToImage`

#### withmarkdown

在图片转Base64中我都会加入Markdown语法, 那我转回来的时候, 肯定也会遇到带有Markdown语法的Base64编码
这个参数就是选择是否开启正则匹配过滤Markdown语法
一般情况是开启的, 因为即使没有含有Markdown语法, 也只是正则匹配返回为空而已, 并不会影响原本的功能

但是如果有Markdown语法的话, 程序会检测 `[test]:data:image/avif;base64,` 中标注得到文件格式
虽然我有写通过Base64的图片编码, 来判断文件类型(这里 `.avif` 并不会被这种方式检测出来, 所以我默认没有检测出来生成的是 `.avif` 格式)

## 开始使用

脚本采用传入参数的形式, 给程序给定待处理目录/文件路径

如果使用exe文件, 可以直接将待处理目录/文件拖拽到exe文件上, 或者用命令行传入参数运行程序

如果使用py脚本, 也是通过命令行传入参数

### 生成配置文件

如果没有配置文件的话, 就随便给一个待处理目录/文件, 当程序没有找到ini文件, 就会自己生成一个

### 日志文件

记录这脚本的转换记录, 如果程序没有反应, 其的报错也会保存在其中

### 程序运行

根据转入的文件类型会进行不同的处理

如果是 `.txt` 就会执行 `Base64ToImage` 模块, 将Base64代码转为Image

如果是 [`defaultformat`](#defaultformat) 中指定的图片类型, 则执行 `ImageToBase64`, 直接将这个图片转为Base64

如果是其他图片类型, 先执行 `ImageToIamge`, 将这个图片的格式转化为[`defaultformat`](#defaultformat) 中指定的图片类型, 再执行 `ImageToBase64`, 将新生成的图片转为Base64

### 生成的文件保存位置

如果传入的是文件, 则会在传入文件的同级目录下, 生成新文件

如果传入的是目录, 则会在传入目录的同级目录下, 生成新目录, 新目录名为原目录名加 `-new`
如 `test` -> `test-new`

## Markdown通过Base64添加图片

``` Markdown
...

![这个对应的标签名A][这个是图片无法显示时显示的文本A]

这里还会有其他的内容

![这个对应的标签名B][这个是图片无法显示时显示的文本B]

...

![这个对应的标签名A][这里还可以复用]

...

下文一般放在文末,方便管理, 上下文之间可以穿插我们的文章内容, 我编写这个脚本就是帮我批量生成下文的内容

[这个对应的标签名A]:data:image/avif;base64,AAAAIGZ0eXBhd...
[这个对应的标签名B]:data:image/avif;base64,AAAAIGZ0eXBhd...
```

从上文应该能明白Markdown通过Base64添加图片的用法吧