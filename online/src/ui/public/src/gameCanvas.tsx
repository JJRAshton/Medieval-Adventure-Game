import React, { useRef, useEffect, MutableRefObject } from 'react'

type CanvasProps = {
    draw: any;
    resize: any;
    handleClick: any;
    handleKeyPress: any;
    handleMouseMove: any;
    setStyle: any;
}

const Canvas = (props: CanvasProps) => {
  
  const { draw, resize, handleClick, handleKeyPress, handleMouseMove, setStyle, ...rest } = props;
  const canvasRef: MutableRefObject<HTMLCanvasElement | null> = useRef(null);
  window.addEventListener("keyup", handleKeyPress);

  useEffect(() => {
    
    const canvas = canvasRef.current;
    if (canvas === null) {
        throw new Error("Critical error: Canvas ref was null");
    }
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
    let animationFrameId: number;
    
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