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
public class TCC_Form : Form
{
	private IContainer components;

	[AccessedThroughProperty("ToolTip1")]
	private ToolTip _ToolTip1;

	[AccessedThroughProperty("GroupBox1")]
	private GroupBox _GroupBox1;

	[AccessedThroughProperty("GroupBox2")]
	private GroupBox _GroupBox2;

	[AccessedThroughProperty("MinTCC")]
	private BCGridControl _MinTCC;

	[AccessedThroughProperty("CheckBox1")]
	private CheckBox _CheckBox1;

	[AccessedThroughProperty("WOTStayLocked")]
	private CheckBox _WOTStayLocked;

	[AccessedThroughProperty("Label18")]
	private Label _Label18;

	[AccessedThroughProperty("WOTLockRPM")]
	private NumericUpDown _WOTLockRPM;

	[AccessedThroughProperty("Label2")]
	private Label _Label2;

	[AccessedThroughProperty("Label1")]
	private Label _Label1;

	[AccessedThroughProperty("GroupBox3")]
	private GroupBox _GroupBox3;

	[AccessedThroughProperty("MinTCCrpm")]
	private NumericUpDown _MinTCCrpm;

	[AccessedThroughProperty("Label3")]
	private Label _Label3;

	[AccessedThroughProperty("MinTCCmintps")]
	private NumericUpDown _MinTCCmintps;

	[AccessedThroughProperty("Label4")]
	private Label _Label4;

	[AccessedThroughProperty("Label5")]
	private Label _Label5;

	[AccessedThroughProperty("MinTCCmaxtps")]
	private NumericUpDown _MinTCCmaxtps;

	public ushort Init;

	internal virtual ToolTip ToolTip1
	{
		[DebuggerNonUserCode]
		get
		{
			return _ToolTip1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_ToolTip1 = value;
		}
	}

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

	internal virtual GroupBox GroupBox2
	{
		[DebuggerNonUserCode]
		get
		{
			return _GroupBox2;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_GroupBox2 = value;
		}
	}

	internal virtual BCGridControl MinTCC
	{
		[DebuggerNonUserCode]
		get
		{
			return _MinTCC;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_MinTCC = value;
		}
	}

	internal virtual CheckBox CheckBox1
	{
		[DebuggerNonUserCode]
		get
		{
			return _CheckBox1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = CheckBox1_CheckedChanged;
			if (_CheckBox1 != null)
			{
				_CheckBox1.CheckedChanged -= eventHandler;
			}
			_CheckBox1 = value;
			if (_CheckBox1 != null)
			{
				_CheckBox1.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual CheckBox WOTStayLocked
	{
		[DebuggerNonUserCode]
		get
		{
			return _WOTStayLocked;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = WOTStayLocked_Click;
			if (_WOTStayLocked != null)
			{
				((Control)_WOTStayLocked).Click -= eventHandler;
			}
			_WOTStayLocked = value;
			if (_WOTStayLocked != null)
			{
				((Control)_WOTStayLocked).Click += eventHandler;
			}
		}
	}

	internal virtual Label Label18
	{
		[DebuggerNonUserCode]
		get
		{
			return _Label18;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Label18 = value;
		}
	}

	internal virtual NumericUpDown WOTLockRPM
	{
		[DebuggerNonUserCode]
		get
		{
			return _WOTLockRPM;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = WOTLockRPM_Click;
			if (_WOTLockRPM != null)
			{
				((Control)_WOTLockRPM).Click -= eventHandler;
			}
			_WOTLockRPM = value;
			if (_WOTLockRPM != null)
			{
				((Control)_WOTLockRPM).Click += eventHandler;
			}
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

	internal virtual GroupBox GroupBox3
	{
		[DebuggerNonUserCode]
		get
		{
			return _GroupBox3;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_GroupBox3 = value;
		}
	}

	internal virtual NumericUpDown MinTCCrpm
	{
		[DebuggerNonUserCode]
		get
		{
			return _MinTCCrpm;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_MinTCCrpm = value;
		}
	}

	internal virtual Label Label3
	{
		[DebuggerNonUserCode]
		get
		{
			return _Label3;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Label3 = value;
		}
	}

	internal virtual NumericUpDown MinTCCmintps
	{
		[DebuggerNonUserCode]
		get
		{
			return _MinTCCmintps;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_MinTCCmintps = value;
		}
	}

	internal virtual Label Label4
	{
		[DebuggerNonUserCode]
		get
		{
			return _Label4;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Label4 = value;
		}
	}

	internal virtual Label Label5
	{
		[DebuggerNonUserCode]
		get
		{
			return _Label5;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Label5 = value;
		}
	}

	internal virtual NumericUpDown MinTCCmaxtps
	{
		[DebuggerNonUserCode]
		get
		{
			return _MinTCCmaxtps;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_MinTCCmaxtps = value;
		}
	}

	public TCC_Form()
	{
		((Form)this).Shown += TCC_Form_Shown;
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
		//IL_0022: Unknown result type (might be due to invalid IL or missing references)
		//IL_002c: Expected O, but got Unknown
		//IL_002d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0037: Expected O, but got Unknown
		//IL_0043: Unknown result type (might be due to invalid IL or missing references)
		//IL_004d: Expected O, but got Unknown
		//IL_004e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0058: Expected O, but got Unknown
		//IL_0059: Unknown result type (might be due to invalid IL or missing references)
		//IL_0063: Expected O, but got Unknown
		//IL_0064: Unknown result type (might be due to invalid IL or missing references)
		//IL_006e: Expected O, but got Unknown
		//IL_006f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0079: Expected O, but got Unknown
		//IL_007a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0084: Expected O, but got Unknown
		//IL_0085: Unknown result type (might be due to invalid IL or missing references)
		//IL_008f: Expected O, but got Unknown
		//IL_0090: Unknown result type (might be due to invalid IL or missing references)
		//IL_009a: Expected O, but got Unknown
		//IL_009b: Unknown result type (might be due to invalid IL or missing references)
		//IL_00a5: Expected O, but got Unknown
		//IL_00a6: Unknown result type (might be due to invalid IL or missing references)
		//IL_00b0: Expected O, but got Unknown
		//IL_00b1: Unknown result type (might be due to invalid IL or missing references)
		//IL_00bb: Expected O, but got Unknown
		//IL_00bc: Unknown result type (might be due to invalid IL or missing references)
		//IL_00c6: Expected O, but got Unknown
		//IL_00c7: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d1: Expected O, but got Unknown
		//IL_00d2: Unknown result type (might be due to invalid IL or missing references)
		//IL_00dc: Expected O, but got Unknown
		//IL_01fc: Unknown result type (might be due to invalid IL or missing references)
		//IL_0206: Expected O, but got Unknown
		//IL_0e48: Unknown result type (might be due to invalid IL or missing references)
		//IL_0e52: Expected O, but got Unknown
		components = new Container();
		ComponentResourceManager componentResourceManager = new ComponentResourceManager(typeof(TCC_Form));
		ToolTip1 = new ToolTip(components);
		Label18 = new Label();
		MinTCC = new BCGridControl();
		WOTStayLocked = new CheckBox();
		CheckBox1 = new CheckBox();
		GroupBox1 = new GroupBox();
		Label2 = new Label();
		Label1 = new Label();
		GroupBox3 = new GroupBox();
		Label5 = new Label();
		MinTCCmaxtps = new NumericUpDown();
		MinTCCmintps = new NumericUpDown();
		Label4 = new Label();
		MinTCCrpm = new NumericUpDown();
		Label3 = new Label();
		GroupBox2 = new GroupBox();
		WOTLockRPM = new NumericUpDown();
		((Control)GroupBox1).SuspendLayout();
		((Control)GroupBox3).SuspendLayout();
		((ISupportInitialize)MinTCCmaxtps).BeginInit();
		((ISupportInitialize)MinTCCmintps).BeginInit();
		((ISupportInitialize)MinTCCrpm).BeginInit();
		((Control)GroupBox2).SuspendLayout();
		((ISupportInitialize)WOTLockRPM).BeginInit();
		((Control)this).SuspendLayout();
		ToolTip1.AutomaticDelay = 25000;
		ToolTip1.AutoPopDelay = 25000;
		ToolTip1.InitialDelay = 1000;
		ToolTip1.ReshowDelay = 1000;
		Label18.AutoSize = true;
		Label label = Label18;
		Point location = new Point(6, 16);
		((Control)label).Location = location;
		((Control)Label18).Name = "Label18";
		Label label2 = Label18;
		Size size = new Size(58, 13);
		((Control)label2).Size = size;
		((Control)Label18).TabIndex = 15;
		Label18.Text = "Lock RPM";
		ToolTip1.SetToolTip((Control)(object)Label18, "Converter WOT lockup RPM. This the target RPM of the engine after the convter locks, not before.");
		((Control)MinTCC).BackgroundImage = (Image)componentResourceManager.GetObject("MinTCC.BackgroundImage");
		((Control)MinTCC).BackgroundImageLayout = (ImageLayout)0;
		MinTCC.Cell_Auto_W = 0;
		MinTCC.Cell_CharMax = 5;
		MinTCC.Cell_CPFormat = "##0.###";
		MinTCC.Cell_FontCLR = Color.Black;
		MinTCC.Cell_Format = "####0";
		MinTCC.Cell_FSelCLR = Color.White;
		MinTCC.Cell_H = 12;
		MinTCC.Cell_HighCLR = Color.RoyalBlue;
		MinTCC.Cell_HSelCLR = Color.DarkRed;
		MinTCC.Cell_LabelFormat = "##0";
		MinTCC.Cell_LowCLR = Color.White;
		MinTCC.Cell_LSelCLR = Color.Red;
		MinTCC.Cell_ShowChanges = 0;
		MinTCC.Cell_W = 32;
		MinTCC.Grid_AxisStatus = 0;
		MinTCC.Grid_DataOffset = 0f;
		MinTCC.Grid_DataScalar = 1f;
		MinTCC.Grid_DataSCopyPaste = 1;
		MinTCC.Grid_DataStatus = 2864;
		MinTCC.Grid_FreezeDraw = 0;
		MinTCC.Grid_GraphType = 1;
		MinTCC.Grid_ReDraw = 0;
		MinTCC.Grid_ShowLabels = 1;
		MinTCC.Grid_Transpose = 0;
		MinTCC.Grid_TransposeCopyPaste = 0;
		MinTCC.Grid_VisibleName = "MinTCCRPM";
		MinTCC.Grid_X = 17;
		MinTCC.Grid_Y = 2;
		BCGridControl minTCC = MinTCC;
		location = new Point(93, 19);
		((Control)minTCC).Location = location;
		((Control)MinTCC).Name = "MinTCC";
		BCGridControl minTCC2 = MinTCC;
		size = new Size(577, 37);
		((Control)minTCC2).Size = size;
		((Control)MinTCC).TabIndex = 1;
		ToolTip1.SetToolTip((Control)(object)MinTCC, "Set to a 0 - Downshift before unlock, 1 - Unlock before downshift, or 2 - Unconditional lock.");
		((ButtonBase)WOTStayLocked).AutoSize = true;
		WOTStayLocked.Checked = true;
		WOTStayLocked.CheckState = (CheckState)1;
		CheckBox wOTStayLocked = WOTStayLocked;
		location = new Point(9, 40);
		((Control)wOTStayLocked).Location = location;
		((Control)WOTStayLocked).Name = "WOTStayLocked";
		CheckBox wOTStayLocked2 = WOTStayLocked;
		size = new Size(189, 17);
		((Control)wOTStayLocked2).Size = size;
		((Control)WOTStayLocked).TabIndex = 1;
		((ButtonBase)WOTStayLocked).Text = "Stay locked into subsequent gears";
		ToolTip1.SetToolTip((Control)(object)WOTStayLocked, "Stay locked up after the initial WOT lockup for all remaining gears.");
		((ButtonBase)WOTStayLocked).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox1).AutoSize = true;
		CheckBox checkBox = CheckBox1;
		location = new Point(12, 11);
		((Control)checkBox).Location = location;
		((Control)CheckBox1).Name = "CheckBox1";
		CheckBox checkBox2 = CheckBox1;
		size = new Size(187, 17);
		((Control)checkBox2).Size = size;
		((Control)CheckBox1).TabIndex = 0;
		((ButtonBase)CheckBox1).Text = "Automatically handle WOT lockup";
		ToolTip1.SetToolTip((Control)(object)CheckBox1, "Let the software generically pick the WOT lockup speeds.");
		((ButtonBase)CheckBox1).UseVisualStyleBackColor = true;
		((Control)GroupBox1).Controls.Add((Control)(object)Label2);
		((Control)GroupBox1).Controls.Add((Control)(object)Label1);
		((Control)GroupBox1).Controls.Add((Control)(object)MinTCC);
		GroupBox groupBox = GroupBox1;
		location = new Point(12, 109);
		((Control)groupBox).Location = location;
		((Control)GroupBox1).Name = "GroupBox1";
		GroupBox groupBox2 = GroupBox1;
		size = new Size(684, 68);
		((Control)groupBox2).Size = size;
		((Control)GroupBox1).TabIndex = 0;
		GroupBox1.TabStop = false;
		GroupBox1.Text = "Min Locked RPM vs TPS";
		ToolTip1.SetToolTip((Control)(object)GroupBox1, componentResourceManager.GetString("GroupBox1.ToolTip"));
		Label2.AutoSize = true;
		Label label3 = Label2;
		location = new Point(6, 42);
		((Control)label3).Location = location;
		((Control)Label2).Name = "Label2";
		Label label4 = Label2;
		size = new Size(75, 13);
		((Control)label4).Size = size;
		((Control)Label2).TabIndex = 3;
		Label2.Text = "Unlock Option";
		Label1.AutoSize = true;
		Label label5 = Label1;
		location = new Point(6, 30);
		((Control)label5).Location = location;
		((Control)Label1).Name = "Label1";
		Label label6 = Label1;
		size = new Size(81, 13);
		((Control)label6).Size = size;
		((Control)Label1).TabIndex = 2;
		Label1.Text = "Min RPM          ";
		((Control)GroupBox3).Controls.Add((Control)(object)Label5);
		((Control)GroupBox3).Controls.Add((Control)(object)MinTCCmaxtps);
		((Control)GroupBox3).Controls.Add((Control)(object)MinTCCmintps);
		((Control)GroupBox3).Controls.Add((Control)(object)Label4);
		((Control)GroupBox3).Controls.Add((Control)(object)MinTCCrpm);
		((Control)GroupBox3).Controls.Add((Control)(object)Label3);
		GroupBox groupBox3 = GroupBox3;
		location = new Point(232, 12);
		((Control)groupBox3).Location = location;
		((Control)GroupBox3).Name = "GroupBox3";
		GroupBox groupBox4 = GroupBox3;
		size = new Size(162, 90);
		((Control)groupBox4).Size = size;
		((Control)GroupBox3).TabIndex = 2;
		GroupBox3.TabStop = false;
		GroupBox3.Text = "Min TPS for Locked";
		ToolTip1.SetToolTip((Control)(object)GroupBox3, "Only affects export values on 4 speed transmissions with min tps qualifiers.");
		Label5.AutoSize = true;
		Label label7 = Label5;
		location = new Point(10, 66);
		((Control)label7).Location = location;
		((Control)Label5).Name = "Label5";
		Label label8 = Label5;
		size = new Size(64, 13);
		((Control)label8).Size = size;
		((Control)Label5).TabIndex = 19;
		Label5.Text = "Enable TPS";
		ToolTip1.SetToolTip((Control)(object)Label5, "Above this TPS lockup is allowed.");
		MinTCCmaxtps.DecimalPlaces = 1;
		NumericUpDown minTCCmaxtps = MinTCCmaxtps;
		decimal increment = new decimal(new int[4] { 1, 0, 0, 65536 });
		minTCCmaxtps.Increment = increment;
		NumericUpDown minTCCmaxtps2 = MinTCCmaxtps;
		location = new Point(84, 64);
		((Control)minTCCmaxtps2).Location = location;
		increment = (MinTCCmaxtps.Maximum = new decimal(new int[4] { 50, 0, 0, 0 }));
		((Control)MinTCCmaxtps).Name = "MinTCCmaxtps";
		NumericUpDown minTCCmaxtps3 = MinTCCmaxtps;
		size = new Size(66, 20);
		((Control)minTCCmaxtps3).Size = size;
		((Control)MinTCCmaxtps).TabIndex = 18;
		increment = (MinTCCmaxtps.Value = new decimal(new int[4] { 5, 0, 0, 0 }));
		MinTCCmintps.DecimalPlaces = 1;
		increment = (MinTCCmintps.Increment = new decimal(new int[4] { 1, 0, 0, 65536 }));
		NumericUpDown minTCCmintps = MinTCCmintps;
		location = new Point(84, 44);
		((Control)minTCCmintps).Location = location;
		increment = (MinTCCmintps.Maximum = new decimal(new int[4] { 50, 0, 0, 0 }));
		((Control)MinTCCmintps).Name = "MinTCCmintps";
		NumericUpDown minTCCmintps2 = MinTCCmintps;
		size = new Size(66, 20);
		((Control)minTCCmintps2).Size = size;
		((Control)MinTCCmintps).TabIndex = 17;
		increment = (MinTCCmintps.Value = new decimal(new int[4] { 3, 0, 0, 0 }));
		Label4.AutoSize = true;
		Label label9 = Label4;
		location = new Point(10, 46);
		((Control)label9).Location = location;
		((Control)Label4).Name = "Label4";
		Label label10 = Label4;
		size = new Size(66, 13);
		((Control)label10).Size = size;
		((Control)Label4).TabIndex = 16;
		Label4.Text = "Disable TPS";
		ToolTip1.SetToolTip((Control)(object)Label4, "Below this TPS lockup is disabled.");
		increment = (MinTCCrpm.Increment = new decimal(new int[4] { 50, 0, 0, 0 }));
		NumericUpDown minTCCrpm = MinTCCrpm;
		location = new Point(84, 18);
		((Control)minTCCrpm).Location = location;
		increment = (MinTCCrpm.Maximum = new decimal(new int[4] { 10000, 0, 0, 0 }));
		increment = (MinTCCrpm.Minimum = new decimal(new int[4] { 800, 0, 0, 0 }));
		((Control)MinTCCrpm).Name = "MinTCCrpm";
		NumericUpDown minTCCrpm2 = MinTCCrpm;
		size = new Size(66, 20);
		((Control)minTCCrpm2).Size = size;
		((Control)MinTCCrpm).TabIndex = 15;
		increment = (MinTCCrpm.Value = new decimal(new int[4] { 1250, 0, 0, 0 }));
		Label3.AutoSize = true;
		Label label11 = Label3;
		location = new Point(10, 20);
		((Control)label11).Location = location;
		((Control)Label3).Name = "Label3";
		Label label12 = Label3;
		size = new Size(51, 13);
		((Control)label12).Size = size;
		((Control)Label3).TabIndex = 0;
		Label3.Text = "Min RPM";
		ToolTip1.SetToolTip((Control)(object)Label3, "Minimum RPM for lock at low throttle positions.");
		((Control)GroupBox2).Controls.Add((Control)(object)Label18);
		((Control)GroupBox2).Controls.Add((Control)(object)WOTLockRPM);
		((Control)GroupBox2).Controls.Add((Control)(object)WOTStayLocked);
		GroupBox groupBox5 = GroupBox2;
		location = new Point(12, 34);
		((Control)groupBox5).Location = location;
		((Control)GroupBox2).Name = "GroupBox2";
		GroupBox groupBox6 = GroupBox2;
		size = new Size(205, 69);
		((Control)groupBox6).Size = size;
		((Control)GroupBox2).TabIndex = 1;
		GroupBox2.TabStop = false;
		GroupBox2.Text = "WOT Lockup";
		increment = (WOTLockRPM.Increment = new decimal(new int[4] { 50, 0, 0, 0 }));
		NumericUpDown wOTLockRPM = WOTLockRPM;
		location = new Point(80, 14);
		((Control)wOTLockRPM).Location = location;
		increment = (WOTLockRPM.Maximum = new decimal(new int[4] { 10000, 0, 0, 0 }));
		increment = (WOTLockRPM.Minimum = new decimal(new int[4] { 1000, 0, 0, 0 }));
		((Control)WOTLockRPM).Name = "WOTLockRPM";
		NumericUpDown wOTLockRPM2 = WOTLockRPM;
		size = new Size(66, 20);
		((Control)wOTLockRPM2).Size = size;
		((Control)WOTLockRPM).TabIndex = 14;
		increment = (WOTLockRPM.Value = new decimal(new int[4] { 5000, 0, 0, 0 }));
		SizeF autoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleDimensions = autoScaleDimensions;
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		size = new Size(709, 190);
		((Form)this).ClientSize = size;
		((Control)this).Controls.Add((Control)(object)GroupBox3);
		((Control)this).Controls.Add((Control)(object)GroupBox2);
		((Control)this).Controls.Add((Control)(object)GroupBox1);
		((Control)this).Controls.Add((Control)(object)CheckBox1);
		((Control)this).DoubleBuffered = true;
		((Form)this).FormBorderStyle = (FormBorderStyle)1;
		((Form)this).Icon = (Icon)componentResourceManager.GetObject("$this.Icon");
		((Control)this).Name = "TCC_Form";
		((Form)this).StartPosition = (FormStartPosition)1;
		((Form)this).Text = "Lockup Config";
		((Control)GroupBox1).ResumeLayout(false);
		((Control)GroupBox1).PerformLayout();
		((Control)GroupBox3).ResumeLayout(false);
		((Control)GroupBox3).PerformLayout();
		((ISupportInitialize)MinTCCmaxtps).EndInit();
		((ISupportInitialize)MinTCCmintps).EndInit();
		((ISupportInitialize)MinTCCrpm).EndInit();
		((Control)GroupBox2).ResumeLayout(false);
		((Control)GroupBox2).PerformLayout();
		((ISupportInitialize)WOTLockRPM).EndInit();
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}

	private void Form_Closing(object sender, CancelEventArgs e)
	{
		e.Cancel = true;
		((Control)this).Hide();
	}

	private void TCC_Form_Shown(object sender, EventArgs e)
	{
		Init = 1;
	}

	private void CheckBox1_CheckedChanged(object sender, EventArgs e)
	{
		if (Init >= 1)
		{
			if (CheckBox1.Checked)
			{
				((Control)GroupBox2).Enabled = false;
			}
			else
			{
				((Control)GroupBox2).Enabled = true;
			}
			MyProject.Forms.Main_Form.US = checked((ushort)(MyProject.Forms.Main_Form.US + 1));
		}
	}

	private void WOTLockRPM_Click(object sender, EventArgs e)
	{
		MyProject.Forms.Main_Form.US = checked((ushort)(MyProject.Forms.Main_Form.US + 1));
	}

	private void WOTStayLocked_Click(object sender, EventArgs e)
	{
		MyProject.Forms.Main_Form.US = checked((ushort)(MyProject.Forms.Main_Form.US + 1));
	}
}
