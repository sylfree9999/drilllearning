---
title: css-basic
date: 2018-06-16 21:34:41
tags: [css, concept]
---

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
