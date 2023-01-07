import React, { useRef, useEffect } from 'react'

const Canvas = props => {
  
  const { draw, resize, handleClick, handleKeyPress, handleMouseMove, setStyle, ...rest } = props;
  const canvasRef = useRef(null);
  window.addEventListener("keyup", handleKeyPress);

  useEffect(() => {
    
    const canvas = canvasRef.current;
    canvas.addEventListener("click", (event) => {
        handleClick(
            // Adjust the click to get it relative to the canvas
            event.pageX - canvas.offsetLeft - canvas.clientLeft, 
            event.pageY - canvas.offsetTop - canvas.clientTop
            );
    }, false);
    canvas.addEventListener("mousemove", (event) => {
        handleMouseMove(
            // Adjust the click to get it relative to the canvas
            event.pageX - canvas.offsetLeft - canvas.clientLeft, 
            event.pageY - canvas.offsetTop - canvas.clientTop
            );
    }, false);
    resize(canvas);
    const context = canvas.getContext('2d');
    let animationFrameId;
    
    const render = () => {
      draw(context);
      animationFrameId = window.requestAnimationFrame(render);
    }
    render();
    
    return () => {
      window.cancelAnimationFrame(animationFrameId);
    }
  }, [draw]);
  
  return <canvas ref={canvasRef} width="100" height="400" style={setStyle()} {...rest}/>
}

export default Canvas