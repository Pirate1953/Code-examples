using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Threading;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Diagnostics;
using System.Runtime.InteropServices;

namespace trans_win_csharp
{
    public partial class Form1 : Form
    {
        [DllImport("kernel32.dll", SetLastError = true)]
        public static extern IntPtr OpenProcess(int processAccess, bool bInheritHandle, int processId);

        [DllImport("kernel32.dll", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        static extern bool CloseHandle(IntPtr hObject);

        [DllImport("kernel32.dll", SetLastError = true)]
        public static extern bool ReadProcessMemory(IntPtr pHandle, IntPtr Address, ref float Buffer, int Size, IntPtr NumberofBytesRead);

        //Process
        private Process[] pList;
        private int pId;

        //Read memory
        private IntPtr handle;

        private int BaseAddress;
        private int size;
        private float tempCoord;

        private int bytesRead;

        //Position on the form
        private Point strucPoint;

        //View matrix
        private int VMBaseAddress; // View Matrix address to read the bytes
        private float[] objCoord = new float[3];
        private float[] view_matrix = new float[16];

        //World to screen
        private float[] screenCoords = new float[4];
        private float[] ndc = new float[3];

        public Form1()
        {
            InitializeComponent();
            
            //Init Values start

            FindProccess("iw4sp");
            this.BaseAddress = 0x01B91BA4; //Game object address to read coordinates
            this.size = 4; //Number of bytes to read
            this.bytesRead = 0; //Number of bytes transferred into the specified buffer
            this.VMBaseAddress = 0x0073EAC0; //Base address of view matrix to read

            //Init Values end

            this.TimerHandler.Enabled = true;
        }

        /// <summary>
        /// Finds process by name and stores its id
        /// </summary>
        /// <param name="pName">Process name to find</param>
        private void FindProccess(String pName)
        {
            pList = Process.GetProcesses();
            if (pList.Count() != 0)
            {
                foreach (Process process in pList)
                {
                    if (process.ProcessName == pName)
                    {
                        pId = process.Id;
                        MessageBox.Show("Proccess " + pName + " found!");
                        handle = OpenProcess(0x00000010, false, pId);
                        return;
                    }
                }
            }
            return;
        }

        /// <summary>
        /// Reads bytes from the specified address in the proccess memory, saves bytes to the buffer
        /// </summary>
        private void ReadBytes()
        {
            ReadProcessMemory(handle, (IntPtr)BaseAddress, ref tempCoord, size, (IntPtr)bytesRead);
            objCoord[0] = tempCoord;
            ReadProcessMemory(handle, (IntPtr)(BaseAddress + 4), ref tempCoord, size, (IntPtr)bytesRead);
            objCoord[1] = tempCoord;
            ReadProcessMemory(handle, (IntPtr)(BaseAddress + 4 + 4), ref tempCoord, size, (IntPtr)bytesRead);
            objCoord[2] = tempCoord;
        }

        /// <summary>
        /// Calls ReadBytes function to read bytes from the specified address in the proccess memory and save to the buffer.
        /// Retrieves bytes for the view matrix and sves it to the buffer too, then converts gmae object coordinates to the screen coordinates and draws
        /// </summary>
        /// <param name="sender">Sender object called this event</param>
        /// <param name="e">EventArgs class object, represents the base class for classes that contain event data, and provides a value to use for events that do not include event data</param>
        private void TimerHandler_Tick(object sender, EventArgs e)
        {
            ReadBytes();
            GetViewMatrix();
            if (WorldToScreen() == 1)
            {
                this.ObjectText.Location = strucPoint;
            }
        }

        /// <summary>
        /// Converts coordinates from 3D world of the game to 2D coordinates for the Form, sets Indicator position using converted 2D coordinates, returns 1 - object is visible on form; 0 - otherwise
        /// </summary>
        /// <returns>integer value 1 - object is visible on form; 0 - otherwise</returns>
        private int WorldToScreen()
        {
            screenCoords[0] = objCoord[0] * view_matrix[0] + objCoord[1] * view_matrix[1] + objCoord[2] * view_matrix[2] + view_matrix[3];
            screenCoords[1] = objCoord[0] * view_matrix[4] + objCoord[1] * view_matrix[5] + objCoord[2] * view_matrix[6] + view_matrix[7];
            screenCoords[2] = objCoord[0] * view_matrix[8] + objCoord[1] * view_matrix[9] + objCoord[2] * view_matrix[10] + view_matrix[11];
            screenCoords[3] = objCoord[0] * view_matrix[12] + objCoord[1] * view_matrix[13] + objCoord[2] * view_matrix[14] + view_matrix[15];
            if (screenCoords[3] < 0.1f)
            {
                return 0;
            }
            ndc[0] = screenCoords[0] / screenCoords[3];
            ndc[1] = screenCoords[1] / screenCoords[3];
            ndc[2] = screenCoords[2] / screenCoords[3];
            strucPoint.X = Convert.ToInt32((this.Width / 2 * ndc[0]) + (ndc[0] + this.Width / 2));
            strucPoint.Y = Convert.ToInt32(-(this.Height / 2 * ndc[1]) + (ndc[1] + this.Height / 2));
            return 1;
        }

        /// <summary>
        /// Closes proccess handle when form is closing
        /// </summary>
        /// <param name="sender">Sender object called this event</param>
        /// <param name="e">FormClosingEventArgs class object, provides data for the FormClosing event</param>
        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            CloseHandle(handle);
        }

        /// <summary>
        /// Reads bytes for the view matrix, saves it to the buffer
        /// </summary>
        private void GetViewMatrix()
        {
            for (int i = 0; i < 16; i++)
            {
                ReadProcessMemory(handle, (IntPtr)(VMBaseAddress + (i * 4)), ref tempCoord, size, (IntPtr)bytesRead);
                view_matrix[i] = tempCoord;
            }
        }
    }
}
