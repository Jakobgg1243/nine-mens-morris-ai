import { useEffect, useRef, useState } from "react";
import { Streamlit } from "streamlit-component-lib";

const BASE_SIZE = 640;

function MyComponent({ args }: any) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const containerRef = useRef<HTMLDivElement | null>(null);

  const [canvasSize, setCanvasSize] = useState(640);
  const [selected, setSelected] = useState<number | null>(null);

  const boardState = args?.board ?? Array(24).fill(" ");
  const phase = args?.phase;
  const currentPlayer = args?.current_player;
  const removable = args?.removable || [];
  const ui_mode = args?.ui_mode;
  const lastMove = args?.last_move;

  let from = null;
  let to = null;

  if (lastMove) {
    if (lastMove[0] === "move") {
      from = lastMove[1];
      to = lastMove[2];
    }

    if (lastMove[0] === "place" || lastMove[0] === "remove") {
      to = lastMove[1];
    }
  }

  const pad = 25;
  const mid = 320;
  const medium = 140;
  const inner = 255;

  const points = [
    [pad, pad], [mid, pad], [BASE_SIZE - pad, pad],
    [medium, medium], [mid, medium], [BASE_SIZE - medium, medium],
    [inner, inner], [mid, inner], [BASE_SIZE - inner, inner],
    [pad, mid], [medium, mid], [inner, mid],
    [BASE_SIZE - inner, mid], [BASE_SIZE - medium, mid], [BASE_SIZE - pad, mid],
    [inner, BASE_SIZE - inner], [mid, BASE_SIZE - inner], [BASE_SIZE - inner, BASE_SIZE - inner],
    [medium, BASE_SIZE - medium], [mid, BASE_SIZE - medium], [BASE_SIZE - medium, BASE_SIZE - medium],
    [pad, BASE_SIZE - pad], [mid, BASE_SIZE - pad], [BASE_SIZE - pad, BASE_SIZE - pad],
  ];

  useEffect(() => {
    const updateSize = () => {
      if (!containerRef.current) return;

      const width = containerRef.current.offsetWidth;
      const size = Math.min(width - 20, BASE_SIZE);

      setCanvasSize(size);
    };

    updateSize();
    window.addEventListener("resize", updateSize);

    return () => window.removeEventListener("resize", updateSize);
  }, []);

  const scale = canvasSize / BASE_SIZE;
  const r = 15 * scale;

  const sx = (x: number) => x * scale;
  const sy = (y: number) => y * scale;

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const draw = () => {
      ctx.clearRect(0, 0, canvasSize, canvasSize);

      ctx.fillStyle = "#0a1421";
      ctx.fillRect(0, 0, canvasSize, canvasSize);

      ctx.strokeStyle = "#d2b48c";
      ctx.lineWidth = 6 * scale;

      ctx.strokeRect(pad * scale, pad * scale, canvasSize - 2 * pad * scale, canvasSize - 2 * pad * scale);

      ctx.strokeRect(medium * scale, medium * scale, (BASE_SIZE - 2 * medium) * scale, (BASE_SIZE - 2 * medium) * scale);

      ctx.strokeRect(inner * scale, inner * scale, (BASE_SIZE - 2 * inner) * scale, (BASE_SIZE - 2 * inner) * scale);

      ctx.beginPath();
      ctx.moveTo(pad * scale, mid * scale);
      ctx.lineTo(inner * scale, mid * scale);
      ctx.stroke();

      ctx.beginPath();
      ctx.moveTo((BASE_SIZE - inner) * scale, mid * scale);
      ctx.lineTo((BASE_SIZE - pad) * scale, mid * scale);
      ctx.stroke();

      ctx.beginPath();
      ctx.moveTo(mid * scale, pad * scale);
      ctx.lineTo(mid * scale, inner * scale);
      ctx.stroke();

      ctx.beginPath();
      ctx.moveTo(mid * scale, (BASE_SIZE - inner) * scale);
      ctx.lineTo(mid * scale, (BASE_SIZE - pad) * scale);
      ctx.stroke();

      points.forEach(([x, y], i) => {
        const cx = sx(x);
        const cy = sy(y);

        ctx.fillStyle = "#8b7355";
        ctx.beginPath();
        ctx.arc(cx, cy, r, 0, Math.PI * 2);
        ctx.fill();

        const piece = boardState[i];

        if (piece && piece !== " ") {
          if (ui_mode === "removal" && removable.includes(i)) {
            ctx.strokeStyle = "red";
            ctx.lineWidth = 4 * scale;
            ctx.beginPath();
            ctx.arc(cx, cy, r + 6 * scale, 0, Math.PI * 2);
            ctx.stroke();
          }

          if (selected === i) {
            ctx.strokeStyle = "green";
            ctx.lineWidth = 4 * scale;
            ctx.beginPath();
            ctx.arc(cx, cy, r + 6 * scale, 0, Math.PI * 2);
            ctx.stroke();
          }

          if (i === from || i === to) {
            ctx.strokeStyle = "gold";
            ctx.lineWidth = 5 * scale;
            ctx.beginPath();
            ctx.arc(cx, cy, r + 8 * scale, 0, Math.PI * 2);
            ctx.stroke();
          }

          ctx.fillStyle = "#f5f5f5";
          ctx.font = `bold ${35 * scale}px Arial`;
          ctx.textAlign = "center";
          ctx.textBaseline = "middle";
          ctx.fillText(piece, cx, cy);
        }
      });
    };

    draw();
    Streamlit.setFrameHeight(canvasSize + 80);
  }, [boardState, selected, canvasSize]);

  const handleClick = (e: any) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();

    const cx = e.clientX - rect.left;
    const cy = e.clientY - rect.top;

    let closest = -1;
    let minDist = 10000;

    points.forEach(([px, py], idx) => {
      const d = Math.hypot(px * scale - cx, py * scale - cy);

      if (d < 40 * scale && d < minDist) {
        minDist = d;
        closest = idx;
      }
    });

    if (closest === -1) return;

    if (ui_mode === "removal") {
      if (removable.includes(closest)) {
        Streamlit.setComponentValue({ type: "remove", pos: closest });
      }
      return;
    }

    if (phase === "placement") {
      Streamlit.setComponentValue({ type: "place", pos: closest });
      return;
    }

    if (selected === null) {
      if (boardState[closest] === currentPlayer) {
        setSelected(closest);
      }
    } else {
      Streamlit.setComponentValue({
        type: "move",
        from: selected,
        to: closest,
      });

      setSelected(null);
    }
  };

  return (
    <div
      ref={containerRef}
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        width: "100%",
        margin: "20px 0",
        background: "#3b2b1f",
        padding: "16px",
        borderRadius: 15,
        boxSizing: "border-box",
      }}
    >
      <canvas
        ref={canvasRef}
        width={canvasSize}
        height={canvasSize}
        onClick={handleClick}
        style={{
          width: canvasSize,
          height: canvasSize,
          maxWidth: "100%",
          border: "5px solid #d2b48c",
          borderRadius: 12,
          cursor: "pointer",
          touchAction: "manipulation",
          display: "block",
        }}
      />
    </div>
  );
}

export default MyComponent;