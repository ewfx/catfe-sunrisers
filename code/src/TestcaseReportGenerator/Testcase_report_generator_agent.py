from typing import AsyncGenerator, List, Sequence

from autogen_agentchat.agents import BaseChatAgent # type: ignore
from autogen_agentchat.base import Response # type: ignore
from autogen_agentchat.messages import AgentMessage, ChatMessage, TextMessage # type: ignore
from autogen_core.base import CancellationToken # type: ignore

import json
import pandas as pd
from fpdf import FPDF # type: ignore
import textwrap

class TestcaseReportGeneratorAgent(BaseChatAgent):
    def __init__(self, name: str):
        super().__init__(name, "A Testcase Report Generator agent to execute testcases.")
        self.testcases_executed = []

    @property
    def produced_message_types(self) -> List[type[ChatMessage]]:
        return [TextMessage]
    
    def read_testcases_executed(self):
        with open('Artifacts/test_cases_executed.json', 'r') as f:
            self.testcases_executed = json.load(f)

    def generate_pdf_report(self):
        data = self.testcases_executed
    
        # Convert JSON data to a pandas DataFrame
        df = pd.DataFrame(data)

        # Handle potential KeyError for 'FAIL' status
        try:
            failed_count = df['status'].value_counts()['FAIL']
        except KeyError:
            failed_count = 0

        # Define column configurations
        headers = ["Testcase #", "Endpoint", "Method", "Body", "Expected Output", "Received Output", "Status"]
        column_widths = [20, 60, 20, 50, 50, 50, 20]  # Adjusted widths
        
        # Create a PDF class
        class PDF(FPDF):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.header_data = None
                self.col_widths = None
                self.table_mode = False  # Flag to track if we're in table rendering mode
                self.header_printed = False  # Track if we've already printed headers on this page
                
            def header(self):
                """Add the header on each page"""
                self.set_font("Arial", style="B", size=12)
                self.cell(0, 10, txt="API Test Report", ln=1, align='C')
                
                # DO NOT add table headers here - we'll control them manually
                # This prevents automatic headers on every page
                
            def footer(self):
                """Add page numbers at the bottom"""
                self.set_y(-15)
                self.set_font("Arial", style="I", size=8)
                self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
                
            def print_table_headers(self):
                """Print table headers manually when needed"""
                if self.header_data and self.col_widths:
                    self.set_font("Arial", size=10)
                    self.set_fill_color(200, 200, 200)
                    for header, width in zip(self.header_data, self.col_widths):
                        self.cell(width, 10, txt=header, border=1, fill=True, align='C')
                    self.ln()
                    self.header_printed = True
                
            def add_row(self, data, widths, max_height=10, highlight_idx=None, highlight_color=None):
                """Add a row with consistent height across all cells with multi-line text support"""
                # Enable table mode
                if not self.table_mode:
                    self.table_mode = True
                
                # Calculate required height for all cells
                line_heights = []
                self.set_font("Arial", size=10)
                
                for i, (txt, w) in enumerate(zip(data, widths)):
                    # For cell with long text, calculate required height
                    txt_str = str(txt)
                    lines = self.get_text_lines(txt_str, w)  # Reduced padding
                    height = len(lines) * 6  # approx 6mm per line
                    line_heights.append(max(height, 10))  # Minimum 10mm
                
                row_height = max(line_heights)+3
                
                # Store starting position
                x_start = self.get_x()
                y_start = self.get_y()
                
                # Check if row will exceed page boundary
                if y_start + row_height > self.page_break_trigger:
                    self.add_page()
                    y_start = self.get_y()
                    self.header_printed = False  # Reset header flag for new page
                
                # If we haven't printed headers yet on this page and we're in table mode
                if not self.header_printed and self.table_mode:
                    self.print_table_headers()
                    y_start = self.get_y()  # Update Y position after printing headers
                
                # Draw each cell with consistent height
                for i, (txt, w) in enumerate(zip(data, widths)):
                    # Move to the correct position
                    self.set_xy(x_start, y_start)
                                        
                    txt_str = str(txt)
                    
                    if i == highlight_idx and highlight_color:
                        self.set_fill_color(*highlight_color)
                        self.set_text_color(255, 255, 255)
                        fill = True
                    else:
                        self.set_fill_color(255, 255, 255)
                        self.set_text_color(0, 0, 0)
                        fill = False
                    
                    # Draw cell with border first to ensure consistent sizing
                    self.cell(w, row_height, "", border=1,fill=fill, align='C') 
                    
                    # Draw text inside cell with proper alignment
                    self.set_xy(x_start, y_start)
                    lines = self.get_text_lines(txt_str, w - 2)  # Reduced padding
                    
                    # Calculate vertical centering
                    text_height = len(lines) * 6
                    # y_offset = (row_height - text_height) / 2 if text_height < row_height else 0
                    
                    # Print each line of text with reduced padding
                    current_y = y_start
                    for line in lines:
                        self.set_xy(x_start, current_y)  # Reduced padding
                        self.cell(w, 6, line, 0, 0, 'L' if i == 0 else 'L')  # Reduced padding
                        current_y += 6
                    
                    # Move to next cell position
                    x_start += w
                
                # Move to next row
                self.set_xy(self.l_margin, y_start + row_height)
                
            def get_text_lines(self, text, width):
                """Split text into lines that fit within the given width"""
                if not text:
                    return [""]
                
                # Calculate average character width
                char_width = self.get_string_width("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") / 62
                
                # Estimate max chars per line - add a small buffer to fit more text
                chars_per_line = int(width / char_width) + 5
                
                # Wrap text to fit width
                wrapped_lines = textwrap.wrap(text, width=chars_per_line)
                
                # If no wrapping occurred (text is shorter than width)
                if not wrapped_lines:
                    wrapped_lines = [text]
                    
                return wrapped_lines
                
            def exit_table_mode(self):
                """Exit table mode for summary section"""
                self.table_mode = False
                self.header_printed = False

        # Create PDF instance
        pdf = PDF(orientation='L', unit='mm', format='A4')
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.header_data = headers
        pdf.col_widths = column_widths
        pdf.add_page()
        
        # Add rows for each test case
        for index, row in df.iterrows():
            # Prepare cell data
            body_text = json.dumps(row['body'], ensure_ascii=False)
            expected_text = row['expectedOutput']
            received_text = row['receivedOutput']
            
            row_data = [
                str(index+1),
                row['endpoint'],
                row['method'],
                body_text,
                expected_text,
                received_text,
                row['status']
            ]
            
            highlight_color = (0, 128, 0) if row['status'] == "PASS" else (255, 0, 0)
            pdf.add_row(row_data, column_widths, highlight_idx=6, highlight_color=highlight_color)

        # Exit table mode for summary
        pdf.exit_table_mode()
            
        # Always start summary on a new page to ensure visibility
        pdf.add_page()
            
        # Add summary section with more prominent styling
        pdf.set_font("Arial", style="B", size=16)
        pdf.cell(0, 15, txt="Test Summary", ln=1, align='C')
        pdf.ln(5)
        
        # Create a boxed summary with colored backgrounds
        pdf.set_font("Arial", style="B", size=12)
        
        # Summary box
        box_width = 150
        box_height = 15
        box_x = (pdf.w - box_width) / 2  # Center the box
        
        # Total Test Cases
        pdf.set_xy(box_x, pdf.get_y())
        pdf.set_fill_color(220, 220, 220)  # Light gray
        pdf.set_text_color(0, 0, 0)
        pdf.cell(box_width, box_height, f"Total Test Cases: {len(df)}", 1, 1, 'C', True)
        
        # Passed Tests
        passed_count = df['status'].value_counts().get('PASS', 0)
        pdf.set_xy(box_x, pdf.get_y())
        pdf.set_fill_color(150, 200, 150)  # Light green
        pdf.cell(box_width, box_height, f"Passed: {passed_count}", 1, 1, 'C', True)
        
        # Failed Tests
        pdf.set_xy(box_x, pdf.get_y())
        pdf.set_fill_color(250, 150, 150)  # Light red
        pdf.cell(box_width, box_height, f"Failed: {failed_count}", 1, 1, 'C', True)
        
        # Success Rate
        success_rate = round((passed_count / len(df)) * 100, 1) if len(df) > 0 else 0
        pdf.set_xy(box_x, pdf.get_y())
        pdf.set_fill_color(200, 200, 250)  # Light blue
        pdf.cell(box_width, box_height, f"Success Rate: {success_rate}%", 1, 1, 'C', True)

        # Save the PDF
        pdf.output("Artifacts/test_cases_report.pdf")
        print("Report generated: Artifacts/test_cases_report.pdf")
            
    async def on_messages(self, messages: Sequence[ChatMessage], cancellation_token: CancellationToken) -> Response:
        pass

    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        pass


async def run_testcase_report_generator_agent() -> None:
    testcase_executor_agent = TestcaseReportGeneratorAgent("testcase_report_generator_agent")
    testcase_executor_agent.read_testcases_executed()
    testcase_executor_agent.generate_pdf_report()