import flet as ft
import flet.canvas as cv
import cv2
import os
import pandas as pd

class State:
    x: float = 0
    y: float = 0
    width: float = 0
    height: float = 0

state = State()
image_files = []
current_image_index = 0
annot_list = [] 
annot_df = pd.DataFrame(columns=['image_filename','x1','x2','y1','y2'])
save_directory = ""
def main(page: ft.Page):
    page.title = "Flet Image Annotator"
    
        
        
    def select_files(e):
        file_picker.pick_files(allow_multiple=True)

    def on_file_picker_result(e: ft.FilePickerResultEvent):
        global image_files, current_image_index
        if e.files:
            image_files = [file.path for file in e.files if file.path.endswith(('png', 'jpg', 'jpeg'))]
            current_image_index = 0
            load_all_image(image_files)
            if annot_list:
                load_image(annot_list[current_image_index]['FilePath'])
            
    def goto_image(e):
        global current_image_index
        print(e.control.data)
        current_image_index = int(e.control.data)
        load_image(annot_list[current_image_index]['FilePath'])
    def load_all_image(image_files):
        for index, image_file in enumerate(image_files):
            print(image_file)
            
            # Load the image using OpenCV to get its dimensions
            image = cv2.imread(image_file)
            if image is None:
                print(f"Failed to load image {image_file}")
                continue
            
            image_height, image_width, _ = image.shape

            image_preview_rows.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Image(src=image_file, width=100, data=index, semantics_label=index),
                        ft.Text(f"{index}", size=15, text_align=ft.CrossAxisAlignment.CENTER,)
                    ],
                    alignment=ft.CrossAxisAlignment.CENTER),
                    data=index,
                    on_click=goto_image,
                    tooltip=f"{image_file}",
                    # padding=ft.padding.symmetric(horizontal=5, vertical=5),
                    margin=ft.margin.symmetric(horizontal=5)
                )
            )

            source_filename = os.path.basename(image_file)
            annot_list.append({
                'Filename': source_filename,
                "FilePath": image_file,
                'height': image_height,
                'width': image_width,
                'bounding_boxes': []
            })
            
            page.update()
    def load_bounding_boxes():
        print("updating bounding boxs")
        bounding_boxes.controls = []
        rect.visible = False
        bounding_rects = [rect]
        text_labels = []
        for idx,bounding_dict in enumerate(annot_list[current_image_index]['bounding_boxes']):
            def show_only_bounding_box(e):
                print(e.control.data)
                data_index = e.control.data
                for bounding_rect in bounding_rects:
                    bounding_rect.paint = stroke_paint
                    bounding_rect.update()
                bounding_rects[data_index+1].paint = stroke_paint_green
                bounding_rects[data_index+1].update()
            def delete_bounding_box(e):
                data_index = e.control.data
                print(data_index)
                del annot_list[current_image_index]['bounding_boxes'][data_index]
                bounding_rects[data_index+1].visible = False
                bounding_rects[data_index+1].update()
                bounding_boxes.controls[data_index].visible = False
                bounding_boxes.controls[data_index].update()
                load_bounding_boxes()
            def applyLabel(e):
                print(e.control.data)
                print(e.control.value)
                annot_list[current_image_index]['bounding_boxes'][e.control.data]["label"] = e.control.value
                load_bounding_boxes()
            bounding_box = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.ALBUM),
                                title=ft.Text(f"Box {idx}"),
                                subtitle=ft.Text(
                                    f"x1:{bounding_dict['x1']}, x2:{bounding_dict['x2']} x3:{bounding_dict['y1']} x4:{bounding_dict['y2']}"
                                ),
                            ),
                            ft.Row([
                                ft.TextField(label="Label",data=idx,value=bounding_dict['label'],on_submit=applyLabel,on_focus=show_only_bounding_box)
                            ]),
                            ft.Row(
                                [ft.TextButton("Show",on_click=show_only_bounding_box,data=idx), ft.TextButton("Delete",on_click=delete_bounding_box,data=idx)],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ]
                    ),
                    width=400,
                    padding=10,
                )
            )
            bounding_boxes.controls.append(bounding_box)

            
            
            new_rect = cv.Rect(bounding_dict['x1'], bounding_dict['y1'], bounding_dict['x2'] - bounding_dict['x1'], bounding_dict['y2'] - bounding_dict['y1'], paint=stroke_paint)
            new_label = cv.Text(bounding_dict['x1']+ 3, bounding_dict['y1']+3, bounding_dict['label'],style=ft.TextStyle(30,color=ft.colors.RED_900,))
            bounding_rects.append(new_rect)
            text_labels.append(new_label)
        cp.shapes = bounding_rects
        tp.shapes = text_labels
        cp.update()
        tp.update()
        page.update()
        bounding_boxes.update()
    def load_image(image_path):
        image_cp.src = image_path
        aspect_ratio = annot_list[current_image_index]['height']/annot_list[current_image_index]['width']
        image_cp.height = annot_list[current_image_index]['height']
        image_cp.width = annot_list[current_image_index]['width']
        print("selected image annotation: ",current_image_index, annot_list[current_image_index])
        
        rect.visible = False

        
        load_bounding_boxes()

        cp.update()
        for image_preview in image_preview_rows.controls:
            image_preview.bgcolor = ft.colors.PRIMARY
            image_preview.content.controls[1].color = ft.colors.WHITE
        image_preview_rows.controls[current_image_index].bgcolor = ft.colors.GREEN_300
        image_preview_rows.controls[current_image_index].content.controls[1].color = ft.colors.WHITE
        page.update()

    def pan_start(e: ft.DragStartEvent):
        rect.visible = True
        rect.update()
        state.x = e.local_x
        
        state.y = e.local_y
        
        annot_list[current_image_index]['bounding_boxes'].append(
            {
                "label":"",
                "x1":state.x,
                "y1":state.y,
                "x2":0,
                "y2":0
            }
        )
        load_bounding_boxes()

    def pan_update(e: ft.DragUpdateEvent):
        state.width = e.local_x - state.x
        state.height = e.local_y - state.y
        rect.x = state.x
        rect.y = state.y
        rect.width = state.width
        rect.height = state.height

        annot_list[current_image_index]['bounding_boxes'][-1]['x2'] = e.local_x
        
        annot_list[current_image_index]['bounding_boxes'][-1]['y2'] = e.local_y
        load_bounding_boxes()
        cp.update()

        # print(image_preview_rows.controls[current_image_index].content.src)
        image_preview_rows.controls[current_image_index].border = ft.border.all(5, ft.colors.GREEN_600)

    def save_data(save_file_path, annotation_filename):
        try:
            save_data_pb = ft.ProgressBar(width=400)
            save_data_text  = ft.Text("Saving Data..")
            # def annot_filename_handle_close(e):
            #     page.dialog.open = False
            #     page.update()
                
            
            
            save_data_progress_dlg_modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("Saving Data"),
                content=ft.Column([
                    save_data_pb,
                    save_data_text
                ]),
                
                actions_alignment=ft.MainAxisAlignment.END,
                
            )
            page.dialog = save_data_progress_dlg_modal
            
            page.dialog.open = True
            page.update()
            total_files = len(annot_list)
            save_annot_list = [] 
            for index,annotation in enumerate(annot_list):
                image_path = annotation['FilePath']
                print(image_path)
                save_data_text.value = f"Processing: {annotation['Filename']}"
                save_data_text.update()
                # Load the image
                image = cv2.imread(image_path)

                image_height, image_width, _ = image.shape
                original_aspect_ratio = image_width / image_height
                original_width = image_cp.height * original_aspect_ratio

                # Calculate the scale factors
                scale_factor_y = image_height / image_cp.height
                scale_factor_x = image_width / original_width

                # Process each bounding box
                output_annoted_folder = os.path.join(save_file_path,"bouding_box")
                os.makedirs(output_annoted_folder, exist_ok=True)
                output_raw_folder = os.path.join(save_file_path,"raw")
                os.makedirs(output_raw_folder, exist_ok=True)


                output_path = os.path.join(output_raw_folder,f"{os.path.basename(image_path)}")
                cv2.imwrite(output_path, image)
                for bounding_box in annotation['bounding_boxes']:
                    x1 = int(scale_factor_x * bounding_box['x1'])
                    x2 = int(scale_factor_x * bounding_box['x2'])
                    y1 = int(scale_factor_y * bounding_box['y1'])
                    y2 = int(scale_factor_y * bounding_box['y2'])

                    # Draw a rectangle on the image
                    start_point = (x1, y1)  # Top-left corner
                    end_point = (x2, y2)    # Bottom-right corner
                    color = (255, 0, 0)     # Rectangle color (BGR format, here it's blue)
                    thickness = 2           # Thickness of the rectangle borders

                    cv2.rectangle(image, start_point, end_point, color, thickness)
                    
                    output_path = os.path.join(output_annoted_folder,f"annotated_{os.path.basename(image_path)}")
                    cv2.imwrite(output_path, image)
                    print(f"Saved annotated image to {output_path}")
                    
                    save_annot_list.append([annotation['Filename'],x1,x2,y1,y2,bounding_box['label']])
                pb_val = (index/total_files)*101*0.01
                save_data_pb.value = pb_val
                save_data_pb.update()

            save_annot_df = pd.DataFrame(save_annot_list, columns=['Filename', 'x1', 'x2', 'y1', 'y2', 'label'])
            save_annot_df.to_csv(os.path.join(save_file_path,annotation_filename), index=False)

            page.dialog.open = False
            page.update()
            def success_handle_close(e):
                page.dialog.open = False
                page.update()
                

            success_dlg_modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("File Saving Success!"),
                content=ft.Text(f"File Saved to folder : {save_file_path}"),
                actions=[
                    ft.TextButton("Open Folder", on_click=lambda e:os.open()),
                    ft.TextButton("Close", on_click=success_handle_close),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                
            )
            page.dialog = success_dlg_modal
            page.dialog.open = True
            page.update()
        except Exception as e:
            print(e)
            def failed_handle_close(e):
                page.dialog.open = False
                page.update()
                

            failed_dlg_modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("File Saving Failed!"),
                content=ft.Text(f"Error: {e}"),
                actions=[
                    
                    ft.TextButton("Close", on_click=failed_handle_close),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                
            )
            page.dialog = failed_dlg_modal
            page.dialog.open = True
            page.update()
    def save_annotation(e):
        try:
            missing_annot = 0
            for annotation in annot_list:
                if len(annotation['bounding_boxes']) == 0:
                    missing_annot += 1
            
            if missing_annot:
                print("missing annotation")
                def missing_handle_close(e):
                    page.dialog.open = False
                    page.update()
                    print(e.control.text)
                    missing_selection = e.control.text
                    if missing_selection == "Yes":
                        missing_annot = 0
                    else:
                        return
                missing_dlg_modal = ft.AlertDialog(
                    modal=True,
                    title=ft.Text(f"{missing_annot} image annotation is missing."),
                    content=ft.Text("Do you really want to continue?"),
                    actions=[
                        ft.TextButton("Yes", on_click=missing_handle_close),
                        ft.TextButton("No", on_click=missing_handle_close),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                    
                )
                page.dialog = missing_dlg_modal
                page.dialog.open = True
                page.update()
            if not missing_annot:
                def get_save_directory_result(e: ft.FilePickerResultEvent):
                    print(e.path if e.path else "Cancelled!")
                    if e.path:
                        save_directory = e.path

                        def annot_filename_handle_close(e):
                            page.dialog.open = False
                            page.update()
                            print(f"Modal dialog closed with action: {e.control.text}")
                            input_filename = annot_filename_input.value
                            if len(input_filename):
                                input_filename = input_filename.replace(".","_").replace(" ", "_") + ".csv"
                                print(input_filename)

                                save_data(save_directory, input_filename)
                        annot_filename_input = ft.TextField(label="Enter File name")
                        save_annot_filename = ""
                        annot_filename_dlg_modal = ft.AlertDialog(
                            modal=True,
                            title=ft.Text("Enter File Name Without Any Extention"),
                            content=annot_filename_input,
                            actions=[
                                ft.TextButton("Enter", on_click=annot_filename_handle_close),
                                ft.TextButton("No", on_click=annot_filename_handle_close),
                            ],
                            actions_alignment=ft.MainAxisAlignment.END,
                            
                        )
                        page.dialog = annot_filename_dlg_modal
                        
                        page.dialog.open = True
                        page.update()
                        
                select_directory_dialog = ft.FilePicker(on_result=get_save_directory_result)
                page.overlay.extend([select_directory_dialog])
                page.update()
                select_directory_dialog.get_directory_path()

                if(len(save_directory)):
                    print("save Directory selected!")
                else:
                    print("no save directory")

                
            

                # source_filename = os.path.basename(image_path)
                # annot_list[current_image_index]['x1'] = x1
                # annot_list[current_image_index]['x2'] = x2
                # annot_list[current_image_index]['y1'] = y1
                # annot_list[current_image_index]['y2'] = y2
                # print(annot_list[current_image_index])
        except Exception as e:
            print(e)


    def show_image(e):
        image_path = image_cp.src
        save_annotation(image_path)

        # Display the image with OpenCV
        image = cv2.imread(f"annotated_{os.path.basename(image_path)}")
        cv2.imshow("Image with Rectangle", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def next_image(e):
        global current_image_index
        current_image_index = (current_image_index + 1) % len(annot_list)
        load_image(annot_list[current_image_index]['FilePath'])

    def prev_image(e):
        global current_image_index
        current_image_index = (current_image_index - 1) % len(annot_list)
        load_image(annot_list[current_image_index]['FilePath'])
    def apply_rest(e):
        prev_index = current_image_index
        for annot in annot_list[current_image_index+1:]:
            annot['bounding_boxes'] = annot_list[prev_index]['bounding_boxes']
        for image_preview_element in image_preview_rows.controls[current_image_index+1:]:
            image_preview_element.border = ft.border.all(5, ft.colors.GREEN_600)
        image_preview_rows.update()

    stroke_paint = ft.Paint(stroke_width=2,color=ft.colors.WHITE, style=ft.PaintingStyle.STROKE)
    stroke_paint_green = ft.Paint(stroke_width=2,color=ft.colors.GREEN, style=ft.PaintingStyle.STROKE)
    rect = cv.Rect(0, 0, 0, 0, paint=stroke_paint,visible=False)
    image_cp = ft.Image(src='assets/images/dummy.jpg', height=500)
    bounding_rects = [rect]
    text_labels = []
    cp = cv.Canvas(
        bounding_rects,
        content=ft.GestureDetector(
            on_pan_start=pan_start,
            on_pan_update=pan_update,
            drag_interval=10,
        ),
        expand=False,
    )
    tp = cv.Canvas(
        text_labels,
        expand=False,
    )
    image_container = ft.Stack(
        [image_cp, cp,tp],
        expand=True,
        height=500
    )

    select_button = ft.FilledTonalButton("Select Images",icon=ft.icons.IMAGE,icon_color=ft.colors.BLUE_400, on_click=select_files)
    ok_button = ft.FilledTonalButton("Annotate & Save",icon=ft.icons.SAVE,icon_color=ft.colors.GREEN_400, on_click=save_annotation)
    rest_button = ft.FilledTonalButton("Apply Rest",icon=ft.icons.NEXT_PLAN,icon_color=ft.colors.YELLOW_400, on_click=apply_rest)
    next_button = ft.FilledTonalButton("Next Image",icon=ft.icons.NAVIGATE_NEXT,icon_color=ft.colors.WHITE, on_click=next_image)
    prev_button = ft.FilledTonalButton("Previous Image",icon=ft.icons.NAVIGATE_BEFORE,icon_color=ft.colors.WHITE, on_click=prev_image)
    image_preview_rows = ft.Row([
        
                            ],
                            scroll=ft.ScrollMode.ALWAYS
                            )
    controls_container = ft.Container(
        content=ft.Row([
            select_button, prev_button, next_button, rest_button, ok_button
        ])
    )
    bounding_boxes = ft.Row(
        [
            
        ]
        ,scroll=ft.ScrollMode.ALWAYS
    )
    page.add(
        image_container,
        ft.Column([
            bounding_boxes,
            image_preview_rows,
            controls_container
        ])
        
    )
    page.window_maximized = True
    file_picker = ft.FilePicker(on_result=on_file_picker_result)
    page.overlay.append(file_picker)
    page.update()
    

ft.app(main)
