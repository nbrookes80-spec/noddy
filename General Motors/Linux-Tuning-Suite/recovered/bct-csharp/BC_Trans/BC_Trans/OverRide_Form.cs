using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.Runtime.CompilerServices;
using System.Windows.Forms;
using BCGrid;
using BC_Trans.My;
using Microsoft.VisualBasic.CompilerServices;

namespace BC_Trans;

[DesignerGenerated]
public class OverRide_Form : Form
{
	private IContainer components;

	[AccessedThroughProperty("GroupBox1")]
	private GroupBox _GroupBox1;

	[AccessedThroughProperty("Label2")]
	private Label _Label2;

	[AccessedThroughProperty("Label1")]
	private Label _Label1;

	[AccessedThroughProperty("OverRide_Grid")]
	private BCGridControl _OverRide_Grid;

	public ushort Init;

	internal virtual GroupBox GroupBox1
	{
		[DebuggerNonUserCode]
		get
		{
			return _GroupBox1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_GroupBox1 = value;
		}
	}

	internal virtual Label Label2
	{
		[DebuggerNonUserCode]
		get
		{
			return _Label2;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Label2 = value;
		}
	}

	internal virtual Label Label1
	{
		[DebuggerNonUserCode]
		get
		{
			return _Label1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Label1 = value;
		}
	}

	internal virtual BCGridControl OverRide_Grid
	{
		[DebuggerNonUserCode]
		get
		{
			return _OverRide_Grid;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_OverRide_Grid = value;
		}
	}

	public OverRide_Form()
	{
		((Form)this).Load += OverRide_Form_Load;
		((Form)this).Shown += OverRide_Form_Shown;
		((Form)this).Closing += Form_Closing;
		Init = 0;
		InitializeComponent();
	}

	[DebuggerNonUserCode]
	protected override void Dispose(bool disposing)
	{
		try
		{
			if (disposing && components != null)
			{
				components.Dispose();
			}
		}
		finally
		{
			((Form)this).Dispose(disposing);
		}
	}

	[DebuggerStepThrough]
	private void InitializeComponent()
	{
		//IL_001c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0026: Expected O, but got Unknown
		//IL_0027: Unknown result type (might be due to invalid IL or missing references)
		//IL_0031: Expected O, but got Unknown
		//IL_0032: Unknown result type (might be due to invalid IL or missing references)
		//IL_003c: Expected O, but got Unknown
		//IL_01e1: Unknown result type (might be due to invalid IL or missing references)
		//IL_01eb: Expected O, but got Unknown
		components = new Container();
		ComponentResourceManager componentResourceManager = new ComponentResourceManager(typeof(OverRide_Form));
		GroupBox1 = new GroupBox();
		Label2 = new Label();
		Label1 = new Label();
		OverRide_Grid = new BCGridControl();
		((Control)GroupBox1).SuspendLayout();
		((Control)this).SuspendLayout();
		((Control)GroupBox1).Controls.Add((Control)(object)Label2);
		((Control)GroupBox1).Controls.Add((Control)(object)Label1);
		((Control)GroupBox1).Controls.Add((Control)(object)OverRide_Grid);
		GroupBox groupBox = GroupBox1;
		Point location = new Point(12, 12);
		((Control)groupBox).Location = location;
		((Control)GroupBox1).Name = "GroupBox1";
		GroupBox groupBox2 = GroupBox1;
		Size size = new Size(684, 142);
		((Control)groupBox2).Size = size;
		((Control)GroupBox1).TabIndex = 1;
		GroupBox1.TabStop = false;
		GroupBox1.Text = "Shift Slope";
		Label2.AutoSize = true;
		Label label = Label2;
		location = new Point(6, 42);
		((Control)label).Location = location;
		((Control)Label2).Name = "Label2";
		Label label2 = Label2;
		size = new Size(65, 13);
		((Control)label2).Size = size;
		((Control)Label2).TabIndex = 3;
		Label2.Text = "Down Slope";
		Label1.AutoSize = true;
		Label label3 = Label1;
		location = new Point(6, 30);
		((Control)label3).Location = location;
		((Control)Label1).Name = "Label1";
		Label label4 = Label1;
		size = new Size(69, 13);
		((Control)label4).Size = size;
		((Control)Label1).TabIndex = 2;
		Label1.Text = "Up Slope      ";
		((Control)OverRide_Grid).BackgroundImage = (Image)componentResourceManager.GetObject("OverRide_Grid.BackgroundImage");
		((Control)OverRide_Grid).BackgroundImageLayout = (ImageLayout)0;
		OverRide_Grid.Cell_Auto_W = 0;
		OverRide_Grid.Cell_CharMax = 5;
		OverRide_Grid.Cell_CPFormat = "##0.###";
		OverRide_Grid.Cell_FontCLR = Color.Black;
		OverRide_Grid.Cell_Format = "0.00";
		OverRide_Grid.Cell_FSelCLR = Color.White;
		OverRide_Grid.Cell_H = 12;
		OverRide_Grid.Cell_HighCLR = Color.RoyalBlue;
		OverRide_Grid.Cell_HSelCLR = Color.DarkRed;
		OverRide_Grid.Cell_LabelFormat = "##0";
		OverRide_Grid.Cell_LowCLR = Color.White;
		OverRide_Grid.Cell_LSelCLR = Color.Red;
		OverRide_Grid.Cell_ShowChanges = 0;
		OverRide_Grid.Cell_W = 32;
		OverRide_Grid.Grid_AxisStatus = 0;
		OverRide_Grid.Grid_DataOffset = 0f;
		OverRide_Grid.Grid_DataScalar = 1f;
		OverRide_Grid.Grid_DataSCopyPaste = 1;
		OverRide_Grid.Grid_DataStatus = 2907;
		OverRide_Grid.Grid_FreezeDraw = 0;
		OverRide_Grid.Grid_GraphType = 1;
		OverRide_Grid.Grid_ReDraw = 0;
		OverRide_Grid.Grid_ShowLabels = 1;
		OverRide_Grid.Grid_Transpose = 0;
		OverRide_Grid.Grid_TransposeCopyPaste = 0;
		OverRide_Grid.Grid_VisibleName = "Slope Override";
		OverRide_Grid.Grid_X = 17;
		OverRide_Grid.Grid_Y = 8;
		BCGridControl overRide_Grid = OverRide_Grid;
		location = new Point(93, 19);
		((Control)overRide_Grid).Location = location;
		((Control)OverRide_Grid).Name = "OverRide_Grid";
		BCGridControl overRide_Grid2 = OverRide_Grid;
		size = new Size(577, 109);
		((Control)overRide_Grid2).Size = size;
		((Control)OverRide_Grid).TabIndex = 1;
		SizeF autoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleDimensions = autoScaleDimensions;
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		size = new Size(709, 170);
		((Form)this).ClientSize = size;
		((Control)this).Controls.Add((Control)(object)GroupBox1);
		((Control)this).DoubleBuffered = true;
		((Form)this).FormBorderStyle = (FormBorderStyle)1;
		((Form)this).MaximizeBox = false;
		((Control)this).Name = "OverRide_Form";
		((Form)this).StartPosition = (FormStartPosition)1;
		((Form)this).Text = "Shift Slope Manual Override";
		((Control)GroupBox1).ResumeLayout(false);
		((Control)GroupBox1).PerformLayout();
		((Control)this).ResumeLayout(false);
	}

	private void OverRide_Form_Load(object sender, EventArgs e)
	{
		((Form)this).Icon = ((Form)MyProject.Forms.Main_Form).Icon;
	}

	private void Form_Closing(object sender, CancelEventArgs e)
	{
		e.Cancel = true;
		((Control)this).Hide();
	}

	private void OverRide_Form_Shown(object sender, EventArgs e)
	{
		Init = 1;
	}
}
