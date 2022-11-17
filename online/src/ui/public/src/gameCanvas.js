import React, { useRef, useEffect } from 'react'

const Canvas = props => {
  
  const { draw, resize, ...rest } = props;
  const canvasRef = useRef(null);
  
  useEffect(() => {
    
    const canvas = canvasRef.current;
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
  
  return <canvas ref={canvasRef} width="100" height="400" {...rest}/>
}

export default Canvas