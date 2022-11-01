var el = document.getElementById("graph"); // get canvas

var options = {
  percent: el.getAttribute("data-percent") || 0,
  size: el.getAttribute("data-size") || 150,
  lineWidth: el.getAttribute("data-line") || 15,
  rotate: el.getAttribute("data-rotate") || 0,
};

var canvas = document.createElement("canvas");
var span = document.createElement("span");
span.textContent = `${options.percent}%`;

var ctx = canvas.getContext("2d");
canvas.width = canvas.height = options.size;

el.appendChild(span);
el.appendChild(canvas);

ctx.translate(options.size / 2, options.size / 2);
ctx.rotate((-1 / 2 + options.rotate / 180) * Math.PI);

//imd = ctx.getImageData(0, 0, 240, 240);
var radius = (options.size - options.lineWidth) / 2;

var drawCircle = function (color, lineWidth, percent) {
  percent = Math.min(Math.max(0, percent || 1), 1);
  ctx.beginPath();
  ctx.arc(0, 0, radius, 0, Math.PI * 2 * percent, false);
  ctx.strokeStyle = color;
  ctx.lineCap = "round";
  ctx.lineWidth = lineWidth;
  ctx.stroke();
};

drawCircle("#D3D3D3", options.lineWidth, 100 / 100);
drawCircle("#76ce76", options.lineWidth, options.percent / 100);
