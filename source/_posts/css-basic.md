---
title: css-basic
date: 2018-06-16 21:34:41
tags: [css, concept]
---

# 布局(传统display+position+float)
## Display 
1,	`block`占一行
	默认`block`的元素有：
	`div p ul ol li h1 h2 h3 h4 h5 h6`
2,	`inline`只占其content的尺寸，如果没有content，就不会显示
3，	`inline-block`是inline的布局，就是都挤在一行（对外的表现），对内表现为block,就是可以像block元素一样设置宽高等（盒模型数据）


## Position
1,	`static` 就是默认的元素定位
2,	`relative` 相对于<span style="color: red;font-weight: bold;">自己原本的位置</span>,比方说几次方这个东西，就可以用relative来做

如果你不给Relative设置`top left bottom right`, 就相当于什么也没发生过，它就是默认的位置

另外如果你设置了它为relative，就相当于给予了它`z-index`的能力

```css
.square {
	position: relative;
	top : -1px;
	left : 1px;
}
```

<!--more-->

3,	`absolute`	完全绝对定位，一样可以设置`top left bottom right`,但是这些值是以其找到的最近的非static父元素为基准。 如果没有这样的父元素， 它就会以`<html>`为父元素.

关于`absolute`与`relative`:


{% asset_img absolute-inside-relative.png %}

{% asset_img absolute-inside-relative2.png %}

4,	`fixed`	基于window的绝对定位，不随页面滚动发生改变

## Margin缩写
三种：
```
margin:	top right bottom left
margin:	(top/bottom)	(right/left)
margin: top	(right/left)	bottom
```

## Float & Clear
float元素只占自己元素的大小，如果只让一边float会发现原本应该另起一行的div会浮动到其左边

{% asset_img float1.png %}

如果第二个元素也变为float，父元素会消失

{% asset_img float2.png %}

`Clear` property specifies what elements can float beside the cleared element and on which side.
	* none	- Allows floating elements on both sides(default)
	* left/right	- No floating elements allowed on the left/right side
	* inherit	- Inherits the clear value of its parent

如果一个元素float left，然后你定义clear to the left. Floated元素会集序float, 但是cleared 元素会显示在下方。

{% asset_img float3.png %}


如果一个floated元素比它的父节点要高,它就会`overflow`出去，如下：

{% asset_img float4.jpg %}

这个时候就要用`clearfix` <span style="color: red">来撑起父元素的高度</span>

```css
.clearfix::after{
	content:"";
	clear:both;
	display:block;
}
```

## Pseudo-elements(selector::pseudo-element)
可以被用作
	*	Style the first letter, or line, of an element
	*	Insert content before, or after, the **content** of an element

`::before/::after` can be used to insert some content before/after the content of an element.

```css
h1::before{
	content:url(smiley.gif);
}
```
{% asset_img pseudo1.png %}


## 居中

{% asset_img center.png %}

```html
<!DOCTYPE html>
<html>
    <head>
        <title>
            Container
        </title>
        <style type="text/css">
            body {
			margin: 0px;
			font-family: 'Open Sans', sans-serif;
		}
		.bg {
			position: absolute;
			height: 100%;
			width:100%;
		}
		.centered {
 		 position: fixed;
 		 width: 100%;
		 top: 40%;
		}

		.centered div a div {
			display: block;
			width: 120px;
			text-align: center;
			font-size: 12px;
		}

		.centered a {
			text-decoration: none;
		}


		.in {
			display: inline-block;
			text-align: center;
			margin: 0px 10px 0px;
		}
        </style>
    </head>
    <body>
        <div class="bg">
            <div class="centered in">
                <div class="in">
                    <a href="" target="_blank">
                        <img src="https://omni.annalect.com/static/i/ico/lg/digital-inventory.png">
                            <div>
                                Campaign Reporting
                            </div>
                        </img>
                    </a>
                </div>
                <div class="in">
                    <a href="" target="_blank">
                        <img src="https://omni.annalect.com/static/i/ico/lg/digital-inventory.png">
                            <div>
                                Campaign Reporting
                            </div>
                        </img>
                    </a>
                </div>
                <div class="in">
                    <a href="" target="_blank">
                        <img src="https://omni.annalect.com/static/i/ico/lg/digital-inventory.png">
                            <div>
                                Campaign Reporting
                            </div>
                        </img>
                    </a>
                </div>
            </div>
        </div>
    </body>
</html>
```
# Flex布局
[Ref:http://www.ruanyifeng.com/blog/2015/07/flex-grammar.html]

Flex是Flexible Box的缩写，意思为“弹性布局”，为盒模型提供了很大的灵活性
任何一个容器都可以指定为Flex布局
**设为Flex布局以后，子元素的`float`,`clear`和`vertical-align`属性将失效**

## flex基本概念
container: 采用flex布局的元素，称为flex容器
flex-item: container里面所有的子元素自动成为容器成员
main axis: 水平主轴。主轴的开始位置（与边框的交叉点）称为`main start`,结束位置为`main end`
cross axis: 垂直交叉轴。开始位置为`cross start`,结束位置为`cross end`

{%asset_img flex-concept.png%}

## container属性
### flex-direction
决定主轴的方向，就是项目的排列方向
```css
.box {
  flex-direction: row | row-reverse | column | column-reverse;
}
```
    *   row(默认值)：主轴为水平方向，起点在左端
    *   row-reverse：主轴为水平方向，起点在右端
    *   column：主轴为垂直方向，起点在上沿
    *   column-reverse：主轴为垂直方向，起点在下沿

{%asset_img flex-direction.png%}

### flex-wrap属性
默认情况下，项目都排在一条线（又称"轴线"）上。`flex-wrap`属性定义，如果一条轴线排不下，如何换行。

```css
.box{
  flex-wrap: nowrap | wrap | wrap-reverse;
}
```
    *   nowrap(默认)：不换行
    {%asset_img flex-nowrap.png%}
    *   wrap:换行，第一行在上方
    {%asset_img flex-wrap.jpg%}
    *   wrap-reverse:换行，第一行在下方
    {%asset_img flex-wrap-reverse.jpg%}

### flex-flow属性
是flex-direction属性和flex-wrap属性的简写形式，默认值为row nowrap。
```css
.box {
  flex-flow: <flex-direction> || <flex-wrap>;
}
```
### justify-content属性
justify-content属性定义了项目在主轴上的对齐方式。
```css
.box {
  justify-content: flex-start | flex-end | center | space-between | space-around;
}
```
{%asset_img flex-justify-content.png%}
    *   flex-start（默认值）：左对齐
    *   flex-end：右对齐
    *   center： 居中
    *   space-between：两端对齐，项目之间的间隔都相等。
    *   space-around：每个项目两侧的间隔相等。所以，项目之间的间隔比项目与边框的间隔大一倍。

### align-items属性
align-items属性定义项目在交叉轴上如何对齐。

```css
.box {
  align-items: flex-start | flex-end | center | baseline | stretch;
}
```
{%asset_img flex-align-items.png%}
    *   flex-start：交叉轴的起点对齐。
    *   flex-end：交叉轴的终点对齐。
    *   center：交叉轴的中点对齐。
    *   baseline: 项目的第一行文字的基线对齐。
    *   stretch（默认值）：如果项目未设置高度或设为auto，将占满整个容器的高度。

### align-content属性
align-content属性定义了多根轴线的对齐方式。如果项目只有一根轴线，该属性不起作用。

```css
.box {
  align-content: flex-start | flex-end | center | space-between | space-around | stretch;
}
```
{%asset_img flex-align-content.png%}
    *   flex-start：与交叉轴的起点对齐。
    *   flex-end：与交叉轴的终点对齐。
    *   center：与交叉轴的中点对齐。
    *   space-between：与交叉轴两端对齐，轴线之间的间隔平均分布。
    *   space-around：每根轴线两侧的间隔都相等。所以，轴线之间的间隔比轴线与边框的间隔大一倍。
    *   stretch（默认值）：轴线占满整个交叉轴。

##item属性
### order属性
order属性定义项目的排列顺序。数值越小，排列越靠前，默认为0。
```css
.item {
  order: <integer>;
}
```


{%asset_img flex-order.png%}
### flex-grow属性
flex-grow属性定义项目的放大比例，默认为0，即如果存在剩余空间，也不放大。
如果所有项目的flex-grow属性都为1，则它们将等分剩余空间（如果有的话）。如果一个项目的flex-grow属性为2，其他项目都为1，则前者占据的剩余空间将比其他项多一倍。

```css
.item {
  flex-grow: <number>; /* default 0 */
}
```
{%asset_img flex-grow.png%}

### flex-shrink属性
flex-shrink属性定义了项目的缩小比例，默认为1，即如果空间不足，该项目将缩小。
如果所有项目的flex-shrink属性都为1，当空间不足时，都将等比例缩小。如果一个项目的flex-shrink属性为0，其他项目都为1，则空间不足时，前者不缩小。
```css
.item {
  flex-shrink: <number>; /* default 1 */
}
```
{%asset_img flex-shrink.jpg%}

### flex-basic属性
flex-basis属性定义了在分配多余空间之前，项目占据的主轴空间（main size）。浏览器根据这个属性，计算主轴是否有多余空间。它的默认值为auto，即项目的本来大小。
它可以设为跟width或height属性一样的值（比如350px），则项目将占据固定空间。

```css
.item {
  flex-basis: <length> | auto; /* default auto */
}
```
### flex属性
flex属性是flex-grow, flex-shrink 和 flex-basis的简写，默认值为0 1 auto。后两个属性可选。

```css
.item {
  flex: none | [ <'flex-grow'> <'flex-shrink'>? || <'flex-basis'> ]
}
```
该属性有两个快捷值：auto (1 1 auto) 和 none (0 0 auto)。

建议优先使用这个属性，而不是单独写三个分离的属性，因为浏览器会推算相关值。

### align-self属性
align-self属性允许单个项目有与其他项目不一样的对齐方式，可覆盖align-items属性。默认值为auto，表示继承父元素的align-items属性，如果没有父元素，则等同于stretch。
```css

.item {
  align-self: auto | flex-start | flex-end | center | baseline | stretch;
}
```

##例子，用flex来垂直居中
```html
<div class="parent">
  <div>Hello!</div>
  <div><p>Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vestibulum tortor quam, feugiat vitae, ultricies eget, tempor sit amet, ante. Donec eu libero sit amet quam egestas semper. Aenean ultricies mi vitae est. Mauris placerat eleifend leo. Quisque sit amet est et sapien ullamcorper pharetra.</p></div>
  <div><img src="https://davidwalsh.name/wp-content/themes/punky/images/logo.png" style="display: inline;"></div>
</div>
```
```css
.parent {
    height:100vh;//very important!
    display: flex;
    justify-content:center;
    align-items: center;
}
div>p{
    padding:1em;
    box-sizing:border-box;
    display:flex;
    border:solid;
    margin:10px;
}
```

# CSS Units
## Absolute Lengths
| Units  | Description  |
|---|---|
| cm  | centimeters  |
| mm  | milimeters  |
| in  | inches (1in = 96px = 2.54cm)  |
| px *  | pixels (1px = 1/96th of 1in)  |
| pt  | points (1pt = 1/72 of 1in)  |
| pc  | picas (1pc = 12 pt)  |

## Relative Lengths
| Unit  | Description  |
|---|---|
| em  | Relative to the font-size of the element (2em means 2 times the size of the current font)  |
| ex  | Relative to the x-height of the current font (rarely used)  |
| ch  | Relative to width of the "0" (zero)  |
| rem  | Relative to font-size of the root element  |
| vw  | Relative to 1% of the width of the viewport*  |
| vh  | Relative to 1% of the height of the viewport*  |
| vmin  | Relative to 1% of viewport's* smaller dimension  |
| vmax  | Relative to 1% of viewport's* larger dimension  |
| %  | Relative to the parent element  |

# Selector

```html
<div id="container">            
   <p>First</p>
    <div>
        <p>Child Paragraph</p>
    </div>
   <p>Second</p>
   <p>Third</p>      
</div>
```

### Space
Descendant selector. 
Target **all p tags** within container div.
例
```css
div#container p{
    font-weight:bold;
}
```

### '>'Sign
Target elements which are **DIRECT** children of a particular element.

```css
div#container > p {
  border: 1px solid black;
}
```
This will target all P element within container div, but **not children of child div**

{%asset_img css_sign.jpg %}

### '+' Sign
This is adjacent sibling combinator. It combines two sequences of simple selectors having the same parent and the second one must come **IMMEDIATELY** after the first. 只会影响到第二个simbling

```css
div + p {  
   color: green;  
} 
```
只会选择div后面紧连着的第一个p，且这个div和p是同级的（共享同一个父亲），也就是说包着`Child Paragraph`的div，和`second`的p是同级的

{%asset_img css_plus.jpg %}

### '~'Sign

Similar to '+' but the difference is that the second selector **does NOT** have to immediately follow the first one. It will select all elements that is preceded by the former selector.

```css
div ~ p{
    background-color:blue;
}
```

{%asset_img css_wave.jpg%}