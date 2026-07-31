from ultralytics import YOLO
import time


model = YOLO("yolov8n.pt")


def detect(image_path):

    start_time = time.perf_counter()

    results = model(image_path)

    end_time = time.perf_counter()

    analysis_time = end_time - start_time

    result = results[0]

    annotated_image = result.plot()

    counts = {}
    
    text = ""

    for box in result.boxes:

        class_id = int(box.cls[0])

        confidence = float(box.conf[0])*100

        name = model.names[class_id]

        if confidence > 30:

            text += f"{name} ({confidence:.1f}%)\n"

            if name in counts:

                counts[name] += 1

            else:

                counts[name] = 1

    if not counts:
    
        return "No object detected.", annotated_image

    sorted_counts = sorted(
            
        counts.items(),
            
        key=lambda item: item[1],
            
        reverse=True
            
    )

    summary = (

        "Detection Summary\n\n"

        f"Analysis time : {analysis_time:.2f} s\n\n"

        )

    for name, number in sorted_counts:

        summary += f"• {name} : {number}\n"

    final_text = summary + "\nDetailed Detection\n\n" + text

    return final_text, annotated_image
