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
public class Lead_Form : Form
{
	private IContainer components;

	[AccessedThroughProperty("Delay")]
	private BCGridControl _Delay;

	[AccessedThroughProperty("GroupBox1")]
	private GroupBox _GroupBox1;

	[AccessedThroughProperty("Label16")]
	private Label _Label16;

	[AccessedThroughProperty("RWHP")]
	private NumericUpDown _RWHP;

	[AccessedThroughProperty("Label15")]
	private Label _Label15;

	[AccessedThroughProperty("Weight")]
	private NumericUpDown _Weight;

	[AccessedThroughProperty("GroupBox2")]
	private GroupBox _GroupBox2;

	[AccessedThroughProperty("Label1")]
	private Label _Label1;

	[AccessedThroughProperty("TCC_Delay")]
	private NumericUpDown _TCC_Delay;

	[AccessedThroughProperty("Label12")]
	private Label _Label12;

	[AccessedThroughProperty("Label11")]
	private Label _Label11;

	[AccessedThroughProperty("Label10")]
	private Label _Label10;

	[AccessedThroughProperty("Label2")]
	private Label _Label2;

	[AccessedThroughProperty("Down_Time")]
	private NumericUpDown _Down_Time;

	[AccessedThroughProperty("ToolTip1")]
	private ToolTip _ToolTip1;

	[AccessedThroughProperty("GroupBox3")]
	private GroupBox _GroupBox3;

	[AccessedThroughProperty("GroupBox4")]
	private GroupBox _GroupBox4;

	[AccessedThroughProperty("Lead_Radio1")]
	private RadioButton _Lead_Radio1;

	[AccessedThroughProperty("Lead_Radio2")]
	private RadioButton _Lead_Radio2;

	[AccessedThroughProperty("Label19")]
	private Label _Label19;

	[AccessedThroughProperty("Lead")]
	private NumericUpDown _Lead;

	[AccessedThroughProperty("RWHPVisible")]
	private NumericUpDown _RWHPVisible;

	[AccessedThroughProperty("WeightVisible")]
	private NumericUpDown _WeightVisible;

	public ushort Init;

	internal virtual BCGridControl Delay
	{
		[DebuggerNonUserCode]
		get
		{
			return _Delay;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Delay = value;
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

	internal virtual Label Label16
	{
		[DebuggerNonUserCode]
		get
		{
			return _Label16;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Label16 = value;
		}
	}

	internal virtual NumericUpDown RWHP
	{
		[DebuggerNonUserCode]
		get
		{
			return _RWHP;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = RWHP_ValueChanged;
			if (_RWHP != null)
			{
				_RWHP.ValueChanged -= eventHandler;
			}
			_RWHP = value;
			if (_RWHP != null)
			{
				_RWHP.ValueChanged += eventHandler;
			}
		}
	}

	internal virtual Label Label15
	{
		[DebuggerNonUserCode]
		get
		{
			return _Label15;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Label15 = value;
		}
	}

	internal virtual NumericUpDown Weight
	{
		[DebuggerNonUserCode]
		get
		{
			return _Weight;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = Weight_ValueChanged;
			if (_Weight != null)
			{
				_Weight.ValueChanged -= eventHandler;
			}
			_Weight = value;
			if (_Weight != null)
			{
				_Weight.ValueChanged += eventHandler;
			}
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

	internal virtual NumericUpDown TCC_Delay
	{
		[DebuggerNonUserCode]
		get
		{
			return _TCC_Delay;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = TCC_Delay_ValueChanged;
			if (_TCC_Delay != null)
			{
				_TCC_Delay.ValueChanged -= eventHandler;
			}
			_TCC_Delay = value;
			if (_TCC_Delay != null)
			{
				_TCC_Delay.ValueChanged += eventHandler;
			}
		}
	}

	internal virtual Label Label12
	{
		[DebuggerNonUserCode]
		get
		{
			return _Label12;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Label12 = value;
		}
	}

	internal virtual Label Label11
	{
		[DebuggerNonUserCode]
		get
		{
			return _Label11;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Label11 = value;
		}
	}

	internal virtual Label Label10
	{
		[DebuggerNonUserCode]
		get
		{
			return _Label10;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Label10 = value;
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

	internal virtual NumericUpDown Down_Time
	{
		[DebuggerNonUserCode]
		get
		{
			return _Down_Time;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = Down_Time_ValueChanged;
			if (_Down_Time != null)
			{
				_Down_Time.ValueChanged -= eventHandler;
			}
			_Down_Time = value;
			if (_Down_Time != null)
			{
				_Down_Time.ValueChanged += eventHandler;
			}
		}
	}

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

	internal virtual GroupBox GroupBox4
	{
		[DebuggerNonUserCode]
		get
		{
			return _GroupBox4;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_GroupBox4 = value;
		}
	}

	internal virtual RadioButton Lead_Radio1
	{
		[DebuggerNonUserCode]
		get
		{
			return _Lead_Radio1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = Lead_Radio1_CheckedChanged;
			if (_Lead_Radio1 != null)
			{
				_Lead_Radio1.CheckedChanged -= eventHandler;
			}
			_Lead_Radio1 = value;
			if (_Lead_Radio1 != null)
			{
				_Lead_Radio1.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual RadioButton Lead_Radio2
	{
		[DebuggerNonUserCode]
		get
		{
			return _Lead_Radio2;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Lead_Radio2 = value;
		}
	}

	internal virtual Label Label19
	{
		[DebuggerNonUserCode]
		get
		{
			return _Label19;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Label19 = value;
		}
	}

	internal virtual NumericUpDown Lead
	{
		[DebuggerNonUserCode]
		get
		{
			return _Lead;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = Lead_ValueChanged_1;
			if (_Lead != null)
			{
				_Lead.ValueChanged -= eventHandler;
			}
			_Lead = value;
			if (_Lead != null)
			{
				_Lead.ValueChanged += eventHandler;
			}
		}
	}

	internal virtual NumericUpDown RWHPVisible
	{
		[DebuggerNonUserCode]
		get
		{
			return _RWHPVisible;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = RWHPVisible_ValueChanged;
			if (_RWHPVisible != null)
			{
				_RWHPVisible.ValueChanged -= eventHandler;
			}
			_RWHPVisible = value;
			if (_RWHPVisible != null)
			{
				_RWHPVisible.ValueChanged += eventHandler;
			}
		}
	}

	internal virtual NumericUpDown WeightVisible
	{
		[DebuggerNonUserCode]
		get
		{
			return _WeightVisible;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = WeightVisible_ValueChanged;
			if (_WeightVisible != null)
			{
				_WeightVisible.ValueChanged -= eventHandler;
			}
			_WeightVisible = value;
			if (_WeightVisible != null)
			{
				_WeightVisible.ValueChanged += eventHandler;
			}
		}
	}

	public Lead_Form()
	{
		((Form)this).Closing += Form_Closing;
		((Form)this).Shown += Lead_Form_Shown;
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
		//IL_0027: Unknown result type (might be due to invalid IL or missing references)
		//IL_0031: Expected O, but got Unknown
		//IL_0032: Unknown result type (might be due to invalid IL or missing references)
		//IL_003c: Expected O, but got Unknown
		//IL_003d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0047: Expected O, but got Unknown
		//IL_0048: Unknown result type (might be due to invalid IL or missing references)
		//IL_0052: Expected O, but got Unknown
		//IL_0053: Unknown result type (might be due to invalid IL or missing references)
		//IL_005d: Expected O, but got Unknown
		//IL_005e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0068: Expected O, but got Unknown
		//IL_0069: Unknown result type (might be due to invalid IL or missing references)
		//IL_0073: Expected O, but got Unknown
		//IL_0074: Unknown result type (might be due to invalid IL or missing references)
		//IL_007e: Expected O, but got Unknown
		//IL_007f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0089: Expected O, but got Unknown
		//IL_008a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0094: Expected O, but got Unknown
		//IL_0095: Unknown result type (might be due to invalid IL or missing references)
		//IL_009f: Expected O, but got Unknown
		//IL_00a0: Unknown result type (might be due to invalid IL or missing references)
		//IL_00aa: Expected O, but got Unknown
		//IL_00ab: Unknown result type (might be due to invalid IL or missing references)
		//IL_00b5: Expected O, but got Unknown
		//IL_00bc: Unknown result type (might be due to invalid IL or missing references)
		//IL_00c6: Expected O, but got Unknown
		//IL_00c7: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d1: Expected O, but got Unknown
		//IL_00d2: Unknown result type (might be due to invalid IL or missing references)
		//IL_00dc: Expected O, but got Unknown
		//IL_00dd: Unknown result type (might be due to invalid IL or missing references)
		//IL_00e7: Expected O, but got Unknown
		//IL_00e8: Unknown result type (might be due to invalid IL or missing references)
		//IL_00f2: Expected O, but got Unknown
		//IL_00f3: Unknown result type (might be due to invalid IL or missing references)
		//IL_00fd: Expected O, but got Unknown
		//IL_00fe: Unknown result type (might be due to invalid IL or missing references)
		//IL_0108: Expected O, but got Unknown
		//IL_0109: Unknown result type (might be due to invalid IL or missing references)
		//IL_0113: Expected O, but got Unknown
		//IL_0114: Unknown result type (might be due to invalid IL or missing references)
		//IL_011e: Expected O, but got Unknown
		//IL_01ae: Unknown result type (might be due to invalid IL or missing references)
		//IL_01b8: Expected O, but got Unknown
		//IL_1349: Unknown result type (might be due to invalid IL or missing references)
		//IL_1353: Expected O, but got Unknown
		components = new Container();
		ComponentResourceManager componentResourceManager = new ComponentResourceManager(typeof(Lead_Form));
		Delay = new BCGridControl();
		GroupBox1 = new GroupBox();
		Label16 = new Label();
		RWHP = new NumericUpDown();
		Label15 = new Label();
		Weight = new NumericUpDown();
		GroupBox2 = new GroupBox();
		Label2 = new Label();
		Down_Time = new NumericUpDown();
		Label12 = new Label();
		Label11 = new Label();
		Label10 = new Label();
		Label1 = new Label();
		TCC_Delay = new NumericUpDown();
		ToolTip1 = new ToolTip(components);
		Label19 = new Label();
		Lead_Radio1 = new RadioButton();
		Lead_Radio2 = new RadioButton();
		GroupBox3 = new GroupBox();
		GroupBox4 = new GroupBox();
		Lead = new NumericUpDown();
		WeightVisible = new NumericUpDown();
		RWHPVisible = new NumericUpDown();
		((Control)GroupBox1).SuspendLayout();
		((ISupportInitialize)RWHP).BeginInit();
		((ISupportInitialize)Weight).BeginInit();
		((Control)GroupBox2).SuspendLayout();
		((ISupportInitialize)Down_Time).BeginInit();
		((ISupportInitialize)TCC_Delay).BeginInit();
		((Control)GroupBox3).SuspendLayout();
		((Control)GroupBox4).SuspendLayout();
		((ISupportInitialize)Lead).BeginInit();
		((ISupportInitialize)WeightVisible).BeginInit();
		((ISupportInitialize)RWHPVisible).BeginInit();
		((Control)this).SuspendLayout();
		((Control)Delay).BackgroundImage = (Image)componentResourceManager.GetObject("Delay.BackgroundImage");
		((Control)Delay).BackgroundImageLayout = (ImageLayout)0;
		Delay.Cell_Auto_W = 0;
		Delay.Cell_CharMax = 5;
		Delay.Cell_CPFormat = "###,###,###,##0.############";
		Delay.Cell_FontCLR = Color.Black;
		Delay.Cell_Format = "##0.00";
		Delay.Cell_FSelCLR = Color.White;
		Delay.Cell_H = 12;
		Delay.Cell_HighCLR = Color.White;
		Delay.Cell_HSelCLR = Color.DarkRed;
		Delay.Cell_LabelFormat = "####0";
		Delay.Cell_LowCLR = Color.White;
		Delay.Cell_LSelCLR = Color.Red;
		Delay.Cell_ShowChanges = 0;
		Delay.Cell_W = 32;
		Delay.Grid_AxisStatus = 0;
		Delay.Grid_DataOffset = 0f;
		Delay.Grid_DataScalar = 1f;
		Delay.Grid_DataSCopyPaste = 1;
		Delay.Grid_DataStatus = 1336;
		Delay.Grid_FreezeDraw = 0;
		Delay.Grid_GraphType = 0;
		Delay.Grid_ReDraw = 0;
		Delay.Grid_ShowLabels = 1;
		Delay.Grid_Transpose = 0;
		Delay.Grid_TransposeCopyPaste = 0;
		Delay.Grid_VisibleName = "Lead Delay";
		Delay.Grid_X = 2;
		Delay.Grid_Y = 11;
		BCGridControl delay = Delay;
		Point location = new Point(30, 64);
		((Control)delay).Location = location;
		((Control)Delay).Name = "Delay";
		BCGridControl delay2 = Delay;
		Size size = new Size(97, 145);
		((Control)delay2).Size = size;
		((Control)Delay).TabIndex = 11;
		ToolTip1.SetToolTip((Control)(object)Delay, "Prep is the amount of time trans takes to prepare for shift. Should be zero for direct clutch transmissions (4Lxx). React is the time between computer commanding shift and it actually taking place.");
		((Control)GroupBox1).Controls.Add((Control)(object)RWHPVisible);
		((Control)GroupBox1).Controls.Add((Control)(object)WeightVisible);
		((Control)GroupBox1).Controls.Add((Control)(object)Label16);
		((Control)GroupBox1).Controls.Add((Control)(object)RWHP);
		((Control)GroupBox1).Controls.Add((Control)(object)Label15);
		((Control)GroupBox1).Controls.Add((Control)(object)Weight);
		GroupBox groupBox = GroupBox1;
		location = new Point(6, 19);
		((Control)groupBox).Location = location;
		((Control)GroupBox1).Name = "GroupBox1";
		GroupBox groupBox2 = GroupBox1;
		size = new Size(135, 70);
		((Control)groupBox2).Size = size;
		((Control)GroupBox1).TabIndex = 12;
		GroupBox1.TabStop = false;
		GroupBox1.Text = "Power to Weight";
		Label16.AutoSize = true;
		Label label = Label16;
		location = new Point(9, 39);
		((Control)label).Location = location;
		((Control)Label16).Name = "Label16";
		Label label2 = Label16;
		size = new Size(37, 13);
		((Control)label2).Size = size;
		((Control)Label16).TabIndex = 21;
		Label16.Text = "Power";
		ToolTip1.SetToolTip((Control)(object)Label16, "RW Power (hp / kw) used inconjunction with weight to estimate acceleration rate.");
		NumericUpDown rWHP = RWHP;
		decimal increment = new decimal(new int[4] { 5, 0, 0, 0 });
		rWHP.Increment = increment;
		NumericUpDown rWHP2 = RWHP;
		location = new Point(68, 37);
		((Control)rWHP2).Location = location;
		increment = (RWHP.Maximum = new decimal(new int[4] { 2000, 0, 0, 0 }));
		increment = (RWHP.Minimum = new decimal(new int[4] { 10, 0, 0, 0 }));
		((Control)RWHP).Name = "RWHP";
		NumericUpDown rWHP3 = RWHP;
		size = new Size(59, 20);
		((Control)rWHP3).Size = size;
		((Control)RWHP).TabIndex = 20;
		increment = (RWHP.Value = new decimal(new int[4] { 300, 0, 0, 0 }));
		((Control)RWHP).Visible = false;
		Label15.AutoSize = true;
		Label label3 = Label15;
		location = new Point(9, 20);
		((Control)label3).Location = location;
		((Control)Label15).Name = "Label15";
		Label label4 = Label15;
		size = new Size(41, 13);
		((Control)label4).Size = size;
		((Control)Label15).TabIndex = 19;
		Label15.Text = "Weight";
		ToolTip1.SetToolTip((Control)(object)Label15, "Weight (lb / kg) used inconjunction with power to estimate acceleration rate.");
		increment = (Weight.Increment = new decimal(new int[4] { 10, 0, 0, 0 }));
		NumericUpDown weight = Weight;
		location = new Point(68, 18);
		((Control)weight).Location = location;
		increment = (Weight.Maximum = new decimal(new int[4] { 25000, 0, 0, 0 }));
		increment = (Weight.Minimum = new decimal(new int[4] { 250, 0, 0, 0 }));
		((Control)Weight).Name = "Weight";
		NumericUpDown weight2 = Weight;
		size = new Size(59, 20);
		((Control)weight2).Size = size;
		((Control)Weight).TabIndex = 18;
		increment = (Weight.Value = new decimal(new int[4] { 3600, 0, 0, 0 }));
		((Control)Weight).Visible = false;
		((Control)GroupBox2).Controls.Add((Control)(object)Label2);
		((Control)GroupBox2).Controls.Add((Control)(object)Down_Time);
		((Control)GroupBox2).Controls.Add((Control)(object)Label12);
		((Control)GroupBox2).Controls.Add((Control)(object)Label11);
		((Control)GroupBox2).Controls.Add((Control)(object)Label10);
		((Control)GroupBox2).Controls.Add((Control)(object)Label1);
		((Control)GroupBox2).Controls.Add((Control)(object)TCC_Delay);
		((Control)GroupBox2).Controls.Add((Control)(object)Delay);
		GroupBox groupBox3 = GroupBox2;
		location = new Point(6, 95);
		((Control)groupBox3).Location = location;
		((Control)GroupBox2).Name = "GroupBox2";
		GroupBox groupBox4 = GroupBox2;
		size = new Size(135, 218);
		((Control)groupBox4).Size = size;
		((Control)GroupBox2).TabIndex = 13;
		GroupBox2.TabStop = false;
		GroupBox2.Text = "Delay Times";
		Label2.AutoSize = true;
		Label label5 = Label2;
		location = new Point(6, 40);
		((Control)label5).Location = location;
		((Control)Label2).Name = "Label2";
		Label label6 = Label2;
		size = new Size(54, 13);
		((Control)label6).Size = size;
		((Control)Label2).TabIndex = 26;
		Label2.Text = "Downshift";
		ToolTip1.SetToolTip((Control)(object)Label2, componentResourceManager.GetString("Label2.ToolTip"));
		Down_Time.DecimalPlaces = 2;
		increment = (Down_Time.Increment = new decimal(new int[4] { 1, 0, 0, 131072 }));
		NumericUpDown down_Time = Down_Time;
		location = new Point(65, 38);
		((Control)down_Time).Location = location;
		increment = (Down_Time.Maximum = new decimal(new int[4] { 4, 0, 0, 0 }));
		((Control)Down_Time).Name = "Down_Time";
		NumericUpDown down_Time2 = Down_Time;
		size = new Size(59, 20);
		((Control)down_Time2).Size = size;
		((Control)Down_Time).TabIndex = 25;
		increment = (Down_Time.Value = new decimal(new int[4] { 5, 0, 0, 65536 }));
		Label12.AutoSize = true;
		Label label7 = Label12;
		location = new Point(91, 62);
		((Control)label7).Location = location;
		((Control)Label12).Name = "Label12";
		Label label8 = Label12;
		size = new Size(36, 13);
		((Control)label8).Size = size;
		((Control)Label12).TabIndex = 24;
		Label12.Text = "React";
		Label11.AutoSize = true;
		Label label9 = Label11;
		location = new Point(63, 62);
		((Control)label9).Location = location;
		((Control)Label11).Name = "Label11";
		Label label10 = Label11;
		size = new Size(29, 13);
		((Control)label10).Size = size;
		((Control)Label11).TabIndex = 23;
		Label11.Text = "Prep";
		Label10.AutoSize = true;
		Label label11 = Label10;
		location = new Point(10, 62);
		((Control)label11).Location = location;
		((Control)Label10).Name = "Label10";
		Label label12 = Label10;
		size = new Size(52, 13);
		((Control)label12).Size = size;
		((Control)Label10).TabIndex = 22;
		Label10.Text = "Upshift to";
		Label1.AutoSize = true;
		Label label13 = Label1;
		location = new Point(6, 16);
		((Control)label13).Location = location;
		((Control)Label1).Name = "Label1";
		Label label14 = Label1;
		size = new Size(58, 13);
		((Control)label14).Size = size;
		((Control)Label1).TabIndex = 21;
		Label1.Text = "TCC Delay";
		ToolTip1.SetToolTip((Control)(object)Label1, "Amount of time from the commanding of lockup and it actually occuring.");
		TCC_Delay.DecimalPlaces = 2;
		increment = (TCC_Delay.Increment = new decimal(new int[4] { 1, 0, 0, 131072 }));
		NumericUpDown tCC_Delay = TCC_Delay;
		location = new Point(65, 14);
		((Control)tCC_Delay).Location = location;
		increment = (TCC_Delay.Maximum = new decimal(new int[4] { 4, 0, 0, 0 }));
		((Control)TCC_Delay).Name = "TCC_Delay";
		NumericUpDown tCC_Delay2 = TCC_Delay;
		size = new Size(59, 20);
		((Control)tCC_Delay2).Size = size;
		((Control)TCC_Delay).TabIndex = 20;
		increment = (TCC_Delay.Value = new decimal(new int[4] { 5, 0, 0, 65536 }));
		ToolTip1.AutomaticDelay = 25000;
		ToolTip1.AutoPopDelay = 25000;
		ToolTip1.InitialDelay = 1000;
		ToolTip1.ReshowDelay = 1000;
		Label19.AutoSize = true;
		Label label15 = Label19;
		location = new Point(6, 18);
		((Control)label15).Location = location;
		((Control)Label19).Name = "Label19";
		Label label16 = Label19;
		size = new Size(31, 13);
		((Control)label16).Size = size;
		((Control)Label19).TabIndex = 15;
		Label19.Text = "Lead";
		ToolTip1.SetToolTip((Control)(object)Label19, componentResourceManager.GetString("Label19.ToolTip"));
		((ButtonBase)Lead_Radio1).AutoSize = true;
		Lead_Radio1.Checked = true;
		RadioButton lead_Radio = Lead_Radio1;
		location = new Point(35, 9);
		((Control)lead_Radio).Location = location;
		((Control)Lead_Radio1).Name = "Lead_Radio1";
		RadioButton lead_Radio2 = Lead_Radio1;
		size = new Size(56, 17);
		((Control)lead_Radio2).Size = size;
		((Control)Lead_Radio1).TabIndex = 17;
		Lead_Radio1.TabStop = true;
		((ButtonBase)Lead_Radio1).Text = "Simple";
		ToolTip1.SetToolTip((Control)(object)Lead_Radio1, "Legacy shift lead management");
		((ButtonBase)Lead_Radio1).UseVisualStyleBackColor = true;
		((ButtonBase)Lead_Radio2).AutoSize = true;
		RadioButton lead_Radio3 = Lead_Radio2;
		location = new Point(157, 9);
		((Control)lead_Radio3).Location = location;
		((Control)Lead_Radio2).Name = "Lead_Radio2";
		RadioButton lead_Radio4 = Lead_Radio2;
		size = new Size(74, 17);
		((Control)lead_Radio4).Size = size;
		((Control)Lead_Radio2).TabIndex = 18;
		((ButtonBase)Lead_Radio2).Text = "Advanced";
		ToolTip1.SetToolTip((Control)(object)Lead_Radio2, "Lead managment based off of estimated acceleration and time.");
		((ButtonBase)Lead_Radio2).UseVisualStyleBackColor = true;
		((Control)GroupBox3).Controls.Add((Control)(object)GroupBox1);
		((Control)GroupBox3).Controls.Add((Control)(object)GroupBox2);
		GroupBox groupBox5 = GroupBox3;
		location = new Point(121, 23);
		((Control)groupBox5).Location = location;
		((Control)GroupBox3).Name = "GroupBox3";
		GroupBox groupBox6 = GroupBox3;
		size = new Size(150, 320);
		((Control)groupBox6).Size = size;
		((Control)GroupBox3).TabIndex = 14;
		GroupBox3.TabStop = false;
		((Control)GroupBox4).Controls.Add((Control)(object)Label19);
		((Control)GroupBox4).Controls.Add((Control)(object)Lead);
		GroupBox groupBox7 = GroupBox4;
		location = new Point(12, 24);
		((Control)groupBox7).Location = location;
		((Control)GroupBox4).Name = "GroupBox4";
		GroupBox groupBox8 = GroupBox4;
		size = new Size(103, 319);
		((Control)groupBox8).Size = size;
		((Control)GroupBox4).TabIndex = 15;
		GroupBox4.TabStop = false;
		Lead.DecimalPlaces = 2;
		increment = (Lead.Increment = new decimal(new int[4] { 25, 0, 0, 131072 }));
		NumericUpDown lead = Lead;
		location = new Point(47, 18);
		((Control)lead).Location = location;
		increment = (Lead.Maximum = new decimal(new int[4] { 10, 0, 0, 0 }));
		((Control)Lead).Name = "Lead";
		NumericUpDown lead2 = Lead;
		size = new Size(41, 20);
		((Control)lead2).Size = size;
		((Control)Lead).TabIndex = 14;
		increment = (Lead.Value = new decimal(new int[4] { 1, 0, 0, 0 }));
		increment = (WeightVisible.Increment = new decimal(new int[4] { 10, 0, 0, 0 }));
		NumericUpDown weightVisible = WeightVisible;
		location = new Point(68, 18);
		((Control)weightVisible).Location = location;
		increment = (WeightVisible.Maximum = new decimal(new int[4] { 25000, 0, 0, 0 }));
		increment = (WeightVisible.Minimum = new decimal(new int[4] { 250, 0, 0, 0 }));
		((Control)WeightVisible).Name = "WeightVisible";
		NumericUpDown weightVisible2 = WeightVisible;
		size = new Size(59, 20);
		((Control)weightVisible2).Size = size;
		((Control)WeightVisible).TabIndex = 22;
		increment = (WeightVisible.Value = new decimal(new int[4] { 3600, 0, 0, 0 }));
		increment = (RWHPVisible.Increment = new decimal(new int[4] { 5, 0, 0, 0 }));
		NumericUpDown rWHPVisible = RWHPVisible;
		location = new Point(68, 37);
		((Control)rWHPVisible).Location = location;
		increment = (RWHPVisible.Maximum = new decimal(new int[4] { 2000, 0, 0, 0 }));
		increment = (RWHPVisible.Minimum = new decimal(new int[4] { 10, 0, 0, 0 }));
		((Control)RWHPVisible).Name = "RWHPVisible";
		NumericUpDown rWHPVisible2 = RWHPVisible;
		size = new Size(59, 20);
		((Control)rWHPVisible2).Size = size;
		((Control)RWHPVisible).TabIndex = 23;
		increment = (RWHPVisible.Value = new decimal(new int[4] { 300, 0, 0, 0 }));
		SizeF autoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleDimensions = autoScaleDimensions;
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		size = new Size(280, 350);
		((Form)this).ClientSize = size;
		((Control)this).Controls.Add((Control)(object)Lead_Radio2);
		((Control)this).Controls.Add((Control)(object)Lead_Radio1);
		((Control)this).Controls.Add((Control)(object)GroupBox4);
		((Control)this).Controls.Add((Control)(object)GroupBox3);
		((Form)this).FormBorderStyle = (FormBorderStyle)1;
		((Form)this).Icon = (Icon)componentResourceManager.GetObject("$this.Icon");
		((Control)this).Name = "Lead_Form";
		((Form)this).StartPosition = (FormStartPosition)1;
		((Form)this).Text = "Shift Lead Time";
		((Control)GroupBox1).ResumeLayout(false);
		((Control)GroupBox1).PerformLayout();
		((ISupportInitialize)RWHP).EndInit();
		((ISupportInitialize)Weight).EndInit();
		((Control)GroupBox2).ResumeLayout(false);
		((Control)GroupBox2).PerformLayout();
		((ISupportInitialize)Down_Time).EndInit();
		((ISupportInitialize)TCC_Delay).EndInit();
		((Control)GroupBox3).ResumeLayout(false);
		((Control)GroupBox4).ResumeLayout(false);
		((Control)GroupBox4).PerformLayout();
		((ISupportInitialize)Lead).EndInit();
		((ISupportInitialize)WeightVisible).EndInit();
		((ISupportInitialize)RWHPVisible).EndInit();
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}

	private void Form_Closing(object sender, CancelEventArgs e)
	{
		e.Cancel = true;
		((Control)this).Hide();
	}

	private void Lead_ValueChanged_1(object sender, EventArgs e)
	{
		if (Init != 0)
		{
			MyProject.Forms.Main_Form.US = checked((ushort)(MyProject.Forms.Main_Form.US + 1));
		}
	}

	private void Lead_Radio1_CheckedChanged(object sender, EventArgs e)
	{
		checked
		{
			if (Init != 0)
			{
				if (Lead_Radio1.Checked)
				{
					((Control)GroupBox3).Enabled = false;
					((Control)GroupBox4).Enabled = true;
					((Control)Delay).Visible = false;
					MyProject.Forms.Main_Form.US = (ushort)(MyProject.Forms.Main_Form.US + 1);
				}
				else
				{
					((Control)GroupBox3).Enabled = true;
					((Control)GroupBox4).Enabled = false;
					((Control)Delay).Visible = true;
					MyProject.Forms.Main_Form.US = (ushort)(MyProject.Forms.Main_Form.US + 1);
				}
			}
		}
	}

	private void WeightVisible_ValueChanged(object sender, EventArgs e)
	{
		if (Init != 0)
		{
			if (MyProject.Forms.Main_Form.Metric.Checked)
			{
				Weight.Value = new decimal(Convert.ToDouble(WeightVisible.Value) / 0.454);
			}
			else
			{
				Weight.Value = WeightVisible.Value;
			}
			MyProject.Forms.Main_Form.US = checked((ushort)(MyProject.Forms.Main_Form.US + 1));
		}
	}

	private void Weight_ValueChanged(object sender, EventArgs e)
	{
		if (Init != 0)
		{
			if (MyProject.Forms.Main_Form.Metric.Checked)
			{
				WeightVisible.Value = new decimal(Convert.ToDouble(Weight.Value) * 0.454);
			}
			else
			{
				WeightVisible.Value = Weight.Value;
			}
			MyProject.Forms.Main_Form.US = checked((ushort)(MyProject.Forms.Main_Form.US + 1));
		}
	}

	private void RWHPVisible_ValueChanged(object sender, EventArgs e)
	{
		if (Init != 0)
		{
			if (MyProject.Forms.Main_Form.Metric.Checked)
			{
				RWHP.Value = new decimal(Convert.ToDouble(RWHPVisible.Value) / 0.746);
			}
			else
			{
				RWHP.Value = RWHPVisible.Value;
			}
			MyProject.Forms.Main_Form.US = checked((ushort)(MyProject.Forms.Main_Form.US + 1));
		}
	}

	private void RWHP_ValueChanged(object sender, EventArgs e)
	{
		if (Init != 0)
		{
			if (MyProject.Forms.Main_Form.Metric.Checked)
			{
				RWHPVisible.Value = new decimal(Convert.ToDouble(RWHP.Value) * 0.746);
			}
			else
			{
				RWHPVisible.Value = RWHP.Value;
			}
			MyProject.Forms.Main_Form.US = checked((ushort)(MyProject.Forms.Main_Form.US + 1));
		}
	}

	private void TCC_Delay_ValueChanged(object sender, EventArgs e)
	{
		if (Init != 0)
		{
			MyProject.Forms.Main_Form.US = checked((ushort)(MyProject.Forms.Main_Form.US + 1));
		}
	}

	private void Down_Time_ValueChanged(object sender, EventArgs e)
	{
		if (Init != 0)
		{
			MyProject.Forms.Main_Form.US = checked((ushort)(MyProject.Forms.Main_Form.US + 1));
		}
	}

	private void Lead_Form_Shown(object sender, EventArgs e)
	{
		Init = 1;
	}
}
