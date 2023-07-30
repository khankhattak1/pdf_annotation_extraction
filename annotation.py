import streamlit as st
import fitz  # PyMuPDF
import PyMuPDF
import os

def extract_annotations_with_content(pdf_file):
    """
    Extracts annotations and their content (including highlighted, strikethrough, and underline text)
    from a given PDF file.

    Parameters:
        pdf_file (str): The path to the input PDF file.
    Returns:
        list: A list of dictionaries, where each dictionary represents an annotation with keys:
              - "page": The page number (1-indexed) where the annotation is found.
              - "type": The type of annotation (e.g., "highlight", "underline", "note", etc.).
              - "content": The content of the annotation.
              - "rect": The rectangle coordinates (left, top, right, bottom) of the annotation.
    """
    annotations = []  # List to store extracted annotations

    # Open the PDF file
    pdf_document = fitz.open(pdf_file)

    # Iterate through each page of the PDF
    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)

        # Get annotations for the current page
        page_annotations = page.annots()

        # Get all words on the current page
        words = page.get_text("words")

        # Iterate through annotations on the current page
        for annot in page_annotations:
            annotation_type = annot.type[0]  # Annotation type (e.g., "H" for highlight, "T" for text, etc.)
            content = ""

            # Handle highlight, underline, and strikeout annotations
            if annotation_type in [8, 9, 11]:
                # Get the text content under the annotation rectangle
                rect = annot.rect
                words_under_annot = [word for word in words if fitz.Rect(word[:4]).intersects(rect)]
                content = " ".join(word[4] for word in words_under_annot)

            # Extract the content of other annotations if available
            elif annotation_type == 0:  # Text annotation
                content = annot.info.get("content", "")

            annotation_data = {
                "page": page_number + 1,  # Page number starts from 1, not 0
                "type": annotation_type,
                "content": content,
                "rect": annot.rect,  # Rectangle coordinates of the annotation (left, top, right, bottom)
            }

            # Add the annotation data to the list
            annotations.append(annotation_data)

    # Close the PDF document
    pdf_document.close()

    return annotations
def display_annotations_via_streamlit():
    
    st.title("PDF Annotation Extractor")
    st.info("This app allows you to extract annotations from PDF files. With this app Underlined, Strikethrough, Highlightes, Text annotation wil have content displayed")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    st.sidebar.title("Annotation Output Format Meaning")
    st.sidebar.write("page : page noumber")
    st.sidebar.write("type : numerical value")
    st.sidebar.write("content : data annotation is applied to")
    st.sidebar.write("rect : rectangle coordinates(x, y, widthof rectangle, height of rectangle)")

    st.sidebar.title("Annotation Type Meanings")
    st.sidebar.write("0: Text Annotation")
    st.sidebar.write("1: Link Annotation")
    st.sidebar.write("2: FreeText Annotation")
    st.sidebar.write("3: Line Annotation")
    st.sidebar.write("4: Square Annotation")
    st.sidebar.write("5: Circle Annotation")
    st.sidebar.write("6: Polygon Annotation")
    st.sidebar.write("7: PolyLine Annotation")
    st.sidebar.write("8: Highlight Annotation")
    st.sidebar.write("9: Underline Annotation")
    st.sidebar.write("10: Squiggly Annotation")
    st.sidebar.write("11: Strikeout Annotation")
    st.sidebar.write("12: Stamp Annotation")
    st.sidebar.write("13: Caret Annotation")
    st.sidebar.write("14: Ink Annotation")
    st.sidebar.write("15: Popup Annotation")
    st.sidebar.write("16: File Attachment Annotation")
    st.sidebar.write("17: Sound Annotation")
    st.sidebar.write("18: Movie Annotation")
    st.sidebar.write("19: Widget Annotation")
    st.sidebar.write("20: Screen Annotation")
    st.sidebar.write("21: PrinterMark Annotation")
    st.sidebar.write("22: TrapNet Annotation")
    st.sidebar.write("23: Watermark Annotation")
    st.sidebar.write("24: 3D Annotation")
    st.sidebar.write("25: Redact Annotation")
    st.sidebar.write("26: Projection Annotation")

    if uploaded_file:
        # Save the uploaded file temporarily
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())

        annotations_list = extract_annotations_with_content("temp.pdf")

        # Display extracted annotations
        if annotations_list:
            st.header("Extracted Annotations:")
            for annotation in annotations_list:
                st.write(annotation)

            # Add a button to copy all output in normal text format
            if st.button("Copy Annotations as Text"):
                annotations_text = "\n".join([str(annotation) for annotation in annotations_list])
                annotations_text = "\n".join([str(annotation) for annotation in annotations_list])
                annotations_text = annotations_text.replace('{', '')
                annotations_text = annotations_text.replace('}', '')
                annotations_text = annotations_text.replace('\'', '')
                annotations_text = annotations_text.replace('\"', '')
                st.text(annotations_text)

             # Add a button to download all output in normal text format
            if True:
                annotations_text = "\n".join([str(annotation) for annotation in annotations_list])
                annotations_text = "\n".join([str(annotation) for annotation in annotations_list])
                annotations_text = annotations_text.replace('{', '')
                annotations_text = annotations_text.replace('}', '')
                annotations_text = annotations_text.replace('\'', '')
                annotations_text = annotations_text.replace('\"', '')
                pdf_filename = os.path.splitext(uploaded_file.name)[0]
                st.download_button(
                    label=f"Download {pdf_filename}_output.txt",
                    data=annotations_text,
                    file_name=f"{pdf_filename}_output.txt",
                    mime="text/plain"
                )
    
        else:
            st.warning("No annotations found in the uploaded PDF.")

        # Remove the temporary file
        os.remove("temp.pdf")

if __name__ == "__main__":
    # Create a 'static' directory in the current working directory if it doesn't exist

    # Display annotations via streamlit
    display_annotations_via_streamlit()
    