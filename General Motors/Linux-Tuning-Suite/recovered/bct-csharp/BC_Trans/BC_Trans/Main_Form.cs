using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Runtime.CompilerServices;
using System.Windows.Forms;
using BCGrid;
using BC_Trans.My;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.CompilerServices;

namespace BC_Trans;

[DesignerGenerated]
public class Main_Form : Form
{
	public struct Trans_Preset
	{
		public string Name;

		public int Gears;

		public float VSS;

		public float Lead;

		public int[] ExportModes;

		public float[] Ratios;

		public float[] Preps;

		public float[] Reacts;
	}

	public struct Slope_Preset
	{
		public string Name;

		public float Factor;

		public float Offset;

		public float UpF;

		public float DownF;
	}

	private IContainer components;

	[AccessedThroughProperty("U_Shift")]
	private BCGridControl _U_Shift;

	[AccessedThroughProperty("BcGridControl1")]
	private BCGridControl _BcGridControl1;

	[AccessedThroughProperty("D_Shift")]
	private BCGridControl _D_Shift;

	[AccessedThroughProperty("Lock")]
	private BCGridControl _Lock;

	[AccessedThroughProperty("Unlock")]
	private BCGridControl _Unlock;

	[AccessedThroughProperty("Gears")]
	private NumericUpDown _Gears;

	[AccessedThroughProperty("Label1")]
	private Label _Label1;

	[AccessedThroughProperty("Slope")]
	private BCGridControl _Slope;

	[AccessedThroughProperty("GroupBox1")]
	private GroupBox _GroupBox1;

	[AccessedThroughProperty("GroupBox2")]
	private GroupBox _GroupBox2;

	[AccessedThroughProperty("Ratio")]
	private BCGridControl _Ratio;

	[AccessedThroughProperty("ComboBox1")]
	private ComboBox _ComboBox1;

	[AccessedThroughProperty("GroupBox3")]
	private GroupBox _GroupBox3;

	[AccessedThroughProperty("Label3")]
	private Label _Label3;

	[AccessedThroughProperty("Offset")]
	private NumericUpDown _Offset;

	[AccessedThroughProperty("Label2")]
	private Label _Label2;

	[AccessedThroughProperty("Factor")]
	private NumericUpDown _Factor;

	[AccessedThroughProperty("ComboBox2")]
	private ComboBox _ComboBox2;

	[AccessedThroughProperty("Label4")]
	private Label _Label4;

	[AccessedThroughProperty("UpF")]
	private NumericUpDown _UpF;

	[AccessedThroughProperty("Label5")]
	private Label _Label5;

	[AccessedThroughProperty("DownF")]
	private NumericUpDown _DownF;

	[AccessedThroughProperty("Label8")]
	private Label _Label8;

	[AccessedThroughProperty("Label7")]
	private Label _Label7;

	[AccessedThroughProperty("Label6")]
	private Label _Label6;

	[AccessedThroughProperty("Label9")]
	private Label _Label9;

	[AccessedThroughProperty("Speed")]
	private BCGridControl _Speed;

	[AccessedThroughProperty("GroupBox4")]
	private GroupBox _GroupBox4;

	[AccessedThroughProperty("GroupBox5")]
	private GroupBox _GroupBox5;

	[AccessedThroughProperty("RPM")]
	private BCGridControl _RPM;

	[AccessedThroughProperty("Label13")]
	private Label _Label13;

	[AccessedThroughProperty("Label12")]
	private Label _Label12;

	[AccessedThroughProperty("Label11")]
	private Label _Label11;

	[AccessedThroughProperty("Label10")]
	private Label _Label10;

	[AccessedThroughProperty("Label14")]
	private Label _Label14;

	[AccessedThroughProperty("Label16")]
	private Label _Label16;

	[AccessedThroughProperty("Tire")]
	private NumericUpDown _Tire;

	[AccessedThroughProperty("Label15")]
	private Label _Label15;

	[AccessedThroughProperty("Gear")]
	private NumericUpDown _Gear;

	[AccessedThroughProperty("Label17")]
	private Label _Label17;

	[AccessedThroughProperty("VSS")]
	private NumericUpDown _VSS;

	[AccessedThroughProperty("GroupBox6")]
	private GroupBox _GroupBox6;

	[AccessedThroughProperty("Label18")]
	private Label _Label18;

	[AccessedThroughProperty("Stall")]
	private NumericUpDown _Stall;

	[AccessedThroughProperty("Label20")]
	private Label _Label20;

	[AccessedThroughProperty("Idle")]
	private NumericUpDown _Idle;

	[AccessedThroughProperty("Label21")]
	private Label _Label21;

	[AccessedThroughProperty("DRPM")]
	private NumericUpDown _DRPM;

	[AccessedThroughProperty("Label23")]
	private Label _Label23;

	[AccessedThroughProperty("MinLck")]
	private NumericUpDown _MinLck;

	[AccessedThroughProperty("Label25")]
	private Label _Label25;

	[AccessedThroughProperty("WotLck")]
	private NumericUpDown _WotLck;

	[AccessedThroughProperty("Label24")]
	private Label _Label24;

	[AccessedThroughProperty("AclLck")]
	private NumericUpDown _AclLck;

	[AccessedThroughProperty("Timer1")]
	private Timer _Timer1;

	[AccessedThroughProperty("MenuStrip1")]
	private MenuStrip _MenuStrip1;

	[AccessedThroughProperty("FileToolStripMenuItem")]
	private ToolStripMenuItem _FileToolStripMenuItem;

	[AccessedThroughProperty("OpenToolStripMenuItem")]
	private ToolStripMenuItem _OpenToolStripMenuItem;

	[AccessedThroughProperty("SaveToolStripMenuItem")]
	private ToolStripMenuItem _SaveToolStripMenuItem;

	[AccessedThroughProperty("ExportToolStripMenuItem")]
	private ToolStripMenuItem _ExportToolStripMenuItem;

	[AccessedThroughProperty("ExportWindowToolStripMenuItem")]
	private ToolStripMenuItem _ExportWindowToolStripMenuItem;

	[AccessedThroughProperty("OptionsToolStripMenuItem")]
	private ToolStripMenuItem _OptionsToolStripMenuItem;

	[AccessedThroughProperty("Allow4L60WOT4th")]
	private ToolStripMenuItem _Allow4L60WOT4th;

	[AccessedThroughProperty("StallLogic")]
	private ToolStripMenuItem _StallLogic;

	[AccessedThroughProperty("LogicChecksRulesToolStripMenuItem")]
	private ToolStripMenuItem _LogicChecksRulesToolStripMenuItem;

	[AccessedThroughProperty("InitLock")]
	private ToolStripMenuItem _InitLock;

	[AccessedThroughProperty("PreLock")]
	private ToolStripMenuItem _PreLock;

	[AccessedThroughProperty("PostLock")]
	private ToolStripMenuItem _PostLock;

	[AccessedThroughProperty("LockUnlock")]
	private ToolStripMenuItem _LockUnlock;

	[AccessedThroughProperty("UpDown")]
	private ToolStripMenuItem _UpDown;

	[AccessedThroughProperty("ShiftMax")]
	private ToolStripMenuItem _ShiftMax;

	[AccessedThroughProperty("ShiftAndLockMinSpreadsToolStripMenuItem")]
	private ToolStripMenuItem _ShiftAndLockMinSpreadsToolStripMenuItem;

	[AccessedThroughProperty("MinShiftToDownshiftSpreadToolStripMenuItem")]
	private ToolStripMenuItem _MinShiftToDownshiftSpreadToolStripMenuItem;

	[AccessedThroughProperty("Shift_Spread")]
	private ToolStripTextBox _Shift_Spread;

	[AccessedThroughProperty("MinLockToUnlockSpreadToolStripMenuItem")]
	private ToolStripMenuItem _MinLockToUnlockSpreadToolStripMenuItem;

	[AccessedThroughProperty("Lock_Spread")]
	private ToolStripTextBox _Lock_Spread;

	[AccessedThroughProperty("Shift_Lock_Spread")]
	private ToolStripMenuItem _Shift_Lock_Spread;

	[AccessedThroughProperty("Lock_Shift_Spread")]
	private ToolStripTextBox _Lock_Shift_Spread;

	[AccessedThroughProperty("ToolStripMenuItem1")]
	private ToolStripMenuItem _ToolStripMenuItem1;

	[AccessedThroughProperty("Unlock_Shift_Spread")]
	private ToolStripTextBox _Unlock_Shift_Spread;

	[AccessedThroughProperty("Metric")]
	private ToolStripMenuItem _Metric;

	[AccessedThroughProperty("OpenFileDialog1")]
	private OpenFileDialog _OpenFileDialog1;

	[AccessedThroughProperty("SaveFileDialog1")]
	private SaveFileDialog _SaveFileDialog1;

	[AccessedThroughProperty("DynoMode")]
	private ToolStripMenuItem _DynoMode;

	[AccessedThroughProperty("LeadRpm")]
	private ToolStripMenuItem _LeadRpm;

	[AccessedThroughProperty("ToolTip1")]
	private ToolTip _ToolTip1;

	[AccessedThroughProperty("No2CT_6L")]
	private ToolStripMenuItem _No2CT_6L;

	[AccessedThroughProperty("Lead_Button")]
	private Button _Lead_Button;

	[AccessedThroughProperty("TCC_Button")]
	private Button _TCC_Button;

	[AccessedThroughProperty("MaxSpeed_Locked")]
	private ToolStripMenuItem _MaxSpeed_Locked;

	[AccessedThroughProperty("ULckStay")]
	private ToolStripMenuItem _ULckStay;

	[AccessedThroughProperty("Label19")]
	private Label _Label19;

	[AccessedThroughProperty("SGS")]
	private ToolStripMenuItem _SGS;

	[AccessedThroughProperty("TireVisible")]
	private NumericUpDown _TireVisible;

	[AccessedThroughProperty("OverRide_Enable")]
	private CheckBox _OverRide_Enable;

	[AccessedThroughProperty("OverRide_Button")]
	private Button _OverRide_Button;

	[AccessedThroughProperty("OverRideReset_Button")]
	private Button _OverRideReset_Button;

	[AccessedThroughProperty("HelpToolStripMenuItem")]
	private ToolStripMenuItem _HelpToolStripMenuItem;

	[AccessedThroughProperty("AboutToolStripMenuItem")]
	private ToolStripMenuItem _AboutToolStripMenuItem;

	[AccessedThroughProperty("RRM")]
	private ToolStripMenuItem _RRM;

	[AccessedThroughProperty("WOTTCCPrep")]
	private ToolStripMenuItem _WOTTCCPrep;

	[AccessedThroughProperty("TireCalc")]
	private Button _TireCalc;

	private float Stall_Slip;

	private float[] MinSpeed;

	private float[,] MinTCCSpeed;

	private float[] StallBase;

	private object[] StallMin;

	public object Dis_High;

	public object Dis_Low;

	public ushort Init;

	public ushort US;

	public ulong PDC;

	public byte D_SC;

	private List<Trans_Preset> TransPresets;

	private List<Slope_Preset> SlopePresets;

	internal virtual BCGridControl U_Shift
	{
		[DebuggerNonUserCode]
		get
		{
			return _U_Shift;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_U_Shift = value;
		}
	}

	internal virtual BCGridControl BcGridControl1
	{
		[DebuggerNonUserCode]
		get
		{
			return _BcGridControl1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_BcGridControl1 = value;
		}
	}

	internal virtual BCGridControl D_Shift
	{
		[DebuggerNonUserCode]
		get
		{
			return _D_Shift;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_D_Shift = value;
		}
	}

	internal virtual BCGridControl Lock
	{
		[DebuggerNonUserCode]
		get
		{
			return _Lock;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Lock = value;
		}
	}

	internal virtual BCGridControl Unlock
	{
		[DebuggerNonUserCode]
		get
		{
			return _Unlock;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Unlock = value;
		}
	}

	internal virtual NumericUpDown Gears
	{
		[DebuggerNonUserCode]
		get
		{
			return _Gears;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = Gears_ValueChanged;
			if (_Gears != null)
			{
				_Gears.ValueChanged -= eventHandler;
			}
			_Gears = value;
			if (_Gears != null)
			{
				_Gears.ValueChanged += eventHandler;
			}
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

	internal virtual BCGridControl Slope
	{
		[DebuggerNonUserCode]
		get
		{
			return _Slope;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Slope = value;
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

	internal virtual BCGridControl Ratio
	{
		[DebuggerNonUserCode]
		get
		{
			return _Ratio;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = Ratio_click;
			if (_Ratio != null)
			{
				((Control)_Ratio).Click -= eventHandler;
			}
			_Ratio = value;
			if (_Ratio != null)
			{
				((Control)_Ratio).Click += eventHandler;
			}
		}
	}

	internal virtual ComboBox ComboBox1
	{
		[DebuggerNonUserCode]
		get
		{
			return _ComboBox1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = ComboBox1_SelectedIndexChanged;
			if (_ComboBox1 != null)
			{
				_ComboBox1.SelectedIndexChanged -= eventHandler;
			}
			_ComboBox1 = value;
			if (_ComboBox1 != null)
			{
				_ComboBox1.SelectedIndexChanged += eventHandler;
			}
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

	internal virtual NumericUpDown Offset
	{
		[DebuggerNonUserCode]
		get
		{
			return _Offset;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = Offset_ValueChanged;
			if (_Offset != null)
			{
				_Offset.ValueChanged -= eventHandler;
			}
			_Offset = value;
			if (_Offset != null)
			{
				_Offset.ValueChanged += eventHandler;
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

	internal virtual NumericUpDown Factor
	{
		[DebuggerNonUserCode]
		get
		{
			return _Factor;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = Factor_ValueChanged;
			if (_Factor != null)
			{
				_Factor.ValueChanged -= eventHandler;
			}
			_Factor = value;
			if (_Factor != null)
			{
				_Factor.ValueChanged += eventHandler;
			}
		}
	}

	internal virtual ComboBox ComboBox2
	{
		[DebuggerNonUserCode]
		get
		{
			return _ComboBox2;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = ComboBox2_SelectedIndexChanged;
			if (_ComboBox2 != null)
			{
				_ComboBox2.SelectedIndexChanged -= eventHandler;
			}
			_ComboBox2 = value;
			if (_ComboBox2 != null)
			{
				_ComboBox2.SelectedIndexChanged += eventHandler;
			}
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

	internal virtual NumericUpDown UpF
	{
		[DebuggerNonUserCode]
		get
		{
			return _UpF;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = UpF_ValueChanged;
			if (_UpF != null)
			{
				_UpF.ValueChanged -= eventHandler;
			}
			_UpF = value;
			if (_UpF != null)
			{
				_UpF.ValueChanged += eventHandler;
			}
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

	internal virtual NumericUpDown DownF
	{
		[DebuggerNonUserCode]
		get
		{
			return _DownF;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = DownF_ValueChanged;
			if (_DownF != null)
			{
				_DownF.ValueChanged -= eventHandler;
			}
			_DownF = value;
			if (_DownF != null)
			{
				_DownF.ValueChanged += eventHandler;
			}
		}
	}

	internal virtual Label Label8
	{
		[DebuggerNonUserCode]
		get
		{
			return _Label8;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Label8 = value;
		}
	}

	internal virtual Label Label7
	{
		[DebuggerNonUserCode]
		get
		{
			return _Label7;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Label7 = value;
		}
	}

	internal virtual Label Label6
	{
		[DebuggerNonUserCode]
		get
		{
			return _Label6;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Label6 = value;
		}
	}

	internal virtual Label Label9
	{
		[DebuggerNonUserCode]
		get
		{
			return _Label9;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Label9 = value;
		}
	}

	internal virtual BCGridControl Speed
	{
		[DebuggerNonUserCode]
		get
		{
			return _Speed;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Speed = value;
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

	internal virtual GroupBox GroupBox5
	{
		[DebuggerNonUserCode]
		get
		{
			return _GroupBox5;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_GroupBox5 = value;
		}
	}

	internal virtual BCGridControl RPM
	{
		[DebuggerNonUserCode]
		get
		{
			return _RPM;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_RPM = value;
		}
	}

	internal virtual Label Label13
	{
		[DebuggerNonUserCode]
		get
		{
			return _Label13;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Label13 = value;
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

	internal virtual Label Label14
	{
		[DebuggerNonUserCode]
		get
		{
			return _Label14;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Label14 = value;
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

	internal virtual NumericUpDown Tire
	{
		[DebuggerNonUserCode]
		get
		{
			return _Tire;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = Tire_ValueChanged;
			if (_Tire != null)
			{
				_Tire.ValueChanged -= eventHandler;
			}
			_Tire = value;
			if (_Tire != null)
			{
				_Tire.ValueChanged += eventHandler;
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

	internal virtual NumericUpDown Gear
	{
		[DebuggerNonUserCode]
		get
		{
			return _Gear;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = Gear_ValueChanged;
			if (_Gear != null)
			{
				_Gear.ValueChanged -= eventHandler;
			}
			_Gear = value;
			if (_Gear != null)
			{
				_Gear.ValueChanged += eventHandler;
			}
		}
	}

	internal virtual Label Label17
	{
		[DebuggerNonUserCode]
		get
		{
			return _Label17;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Label17 = value;
		}
	}

	internal virtual NumericUpDown VSS
	{
		[DebuggerNonUserCode]
		get
		{
			return _VSS;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = VSS_ValueChanged;
			if (_VSS != null)
			{
				_VSS.ValueChanged -= eventHandler;
			}
			_VSS = value;
			if (_VSS != null)
			{
				_VSS.ValueChanged += eventHandler;
			}
		}
	}

	internal virtual GroupBox GroupBox6
	{
		[DebuggerNonUserCode]
		get
		{
			return _GroupBox6;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_GroupBox6 = value;
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

	internal virtual NumericUpDown Stall
	{
		[DebuggerNonUserCode]
		get
		{
			return _Stall;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = Stall_ValueChanged;
			if (_Stall != null)
			{
				_Stall.ValueChanged -= eventHandler;
			}
			_Stall = value;
			if (_Stall != null)
			{
				_Stall.ValueChanged += eventHandler;
			}
		}
	}

	internal virtual Label Label20
	{
		[DebuggerNonUserCode]
		get
		{
			return _Label20;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Label20 = value;
		}
	}

	internal virtual NumericUpDown Idle
	{
		[DebuggerNonUserCode]
		get
		{
			return _Idle;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = Idle_ValueChanged;
			if (_Idle != null)
			{
				_Idle.ValueChanged -= eventHandler;
			}
			_Idle = value;
			if (_Idle != null)
			{
				_Idle.ValueChanged += eventHandler;
			}
		}
	}

	internal virtual Label Label21
	{
		[DebuggerNonUserCode]
		get
		{
			return _Label21;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Label21 = value;
		}
	}

	internal virtual NumericUpDown DRPM
	{
		[DebuggerNonUserCode]
		get
		{
			return _DRPM;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = DRPM_ValueChanged;
			if (_DRPM != null)
			{
				_DRPM.ValueChanged -= eventHandler;
			}
			_DRPM = value;
			if (_DRPM != null)
			{
				_DRPM.ValueChanged += eventHandler;
			}
		}
	}

	internal virtual Label Label23
	{
		[DebuggerNonUserCode]
		get
		{
			return _Label23;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Label23 = value;
		}
	}

	internal virtual NumericUpDown MinLck
	{
		[DebuggerNonUserCode]
		get
		{
			return _MinLck;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = MinLck_ValueChanged;
			if (_MinLck != null)
			{
				_MinLck.ValueChanged -= eventHandler;
			}
			_MinLck = value;
			if (_MinLck != null)
			{
				_MinLck.ValueChanged += eventHandler;
			}
		}
	}

	internal virtual Label Label25
	{
		[DebuggerNonUserCode]
		get
		{
			return _Label25;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Label25 = value;
		}
	}

	internal virtual NumericUpDown WotLck
	{
		[DebuggerNonUserCode]
		get
		{
			return _WotLck;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = WotLck_ValueChanged;
			if (_WotLck != null)
			{
				_WotLck.ValueChanged -= eventHandler;
			}
			_WotLck = value;
			if (_WotLck != null)
			{
				_WotLck.ValueChanged += eventHandler;
			}
		}
	}

	internal virtual Label Label24
	{
		[DebuggerNonUserCode]
		get
		{
			return _Label24;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Label24 = value;
		}
	}

	internal virtual NumericUpDown AclLck
	{
		[DebuggerNonUserCode]
		get
		{
			return _AclLck;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = AclLck_ValueChanged;
			if (_AclLck != null)
			{
				_AclLck.ValueChanged -= eventHandler;
			}
			_AclLck = value;
			if (_AclLck != null)
			{
				_AclLck.ValueChanged += eventHandler;
			}
		}
	}

	internal virtual Timer Timer1
	{
		[DebuggerNonUserCode]
		get
		{
			return _Timer1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = Timer1_Tick;
			if (_Timer1 != null)
			{
				_Timer1.Tick -= eventHandler;
			}
			_Timer1 = value;
			if (_Timer1 != null)
			{
				_Timer1.Tick += eventHandler;
			}
		}
	}

	internal virtual MenuStrip MenuStrip1
	{
		[DebuggerNonUserCode]
		get
		{
			return _MenuStrip1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_MenuStrip1 = value;
		}
	}

	internal virtual ToolStripMenuItem FileToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _FileToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_FileToolStripMenuItem = value;
		}
	}

	internal virtual ToolStripMenuItem OpenToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _OpenToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = OpenToolStripMenuItem_Click;
			if (_OpenToolStripMenuItem != null)
			{
				((ToolStripItem)_OpenToolStripMenuItem).Click -= eventHandler;
			}
			_OpenToolStripMenuItem = value;
			if (_OpenToolStripMenuItem != null)
			{
				((ToolStripItem)_OpenToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem SaveToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _SaveToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = SaveToolStripMenuItem_Click;
			if (_SaveToolStripMenuItem != null)
			{
				((ToolStripItem)_SaveToolStripMenuItem).Click -= eventHandler;
			}
			_SaveToolStripMenuItem = value;
			if (_SaveToolStripMenuItem != null)
			{
				((ToolStripItem)_SaveToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem ExportToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _ExportToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_ExportToolStripMenuItem = value;
		}
	}

	internal virtual ToolStripMenuItem ExportWindowToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _ExportWindowToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = ExportWindowToolStripMenuItem_Click;
			if (_ExportWindowToolStripMenuItem != null)
			{
				((ToolStripItem)_ExportWindowToolStripMenuItem).Click -= eventHandler;
			}
			_ExportWindowToolStripMenuItem = value;
			if (_ExportWindowToolStripMenuItem != null)
			{
				((ToolStripItem)_ExportWindowToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem OptionsToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _OptionsToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_OptionsToolStripMenuItem = value;
		}
	}

	internal virtual ToolStripMenuItem Allow4L60WOT4th
	{
		[DebuggerNonUserCode]
		get
		{
			return _Allow4L60WOT4th;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = Allow4L60WOT4th_Click;
			if (_Allow4L60WOT4th != null)
			{
				((ToolStripItem)_Allow4L60WOT4th).Click -= eventHandler;
			}
			_Allow4L60WOT4th = value;
			if (_Allow4L60WOT4th != null)
			{
				((ToolStripItem)_Allow4L60WOT4th).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem StallLogic
	{
		[DebuggerNonUserCode]
		get
		{
			return _StallLogic;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = StallLogic_Click;
			if (_StallLogic != null)
			{
				((ToolStripItem)_StallLogic).Click -= eventHandler;
			}
			_StallLogic = value;
			if (_StallLogic != null)
			{
				((ToolStripItem)_StallLogic).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem LogicChecksRulesToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _LogicChecksRulesToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_LogicChecksRulesToolStripMenuItem = value;
		}
	}

	internal virtual ToolStripMenuItem InitLock
	{
		[DebuggerNonUserCode]
		get
		{
			return _InitLock;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = InitLock_Click;
			if (_InitLock != null)
			{
				((ToolStripItem)_InitLock).Click -= eventHandler;
			}
			_InitLock = value;
			if (_InitLock != null)
			{
				((ToolStripItem)_InitLock).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem PreLock
	{
		[DebuggerNonUserCode]
		get
		{
			return _PreLock;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = PreLock_Click;
			if (_PreLock != null)
			{
				((ToolStripItem)_PreLock).Click -= eventHandler;
			}
			_PreLock = value;
			if (_PreLock != null)
			{
				((ToolStripItem)_PreLock).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem PostLock
	{
		[DebuggerNonUserCode]
		get
		{
			return _PostLock;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = PostLock_Click;
			if (_PostLock != null)
			{
				((ToolStripItem)_PostLock).Click -= eventHandler;
			}
			_PostLock = value;
			if (_PostLock != null)
			{
				((ToolStripItem)_PostLock).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem LockUnlock
	{
		[DebuggerNonUserCode]
		get
		{
			return _LockUnlock;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = LockUnlock_Click;
			if (_LockUnlock != null)
			{
				((ToolStripItem)_LockUnlock).Click -= eventHandler;
			}
			_LockUnlock = value;
			if (_LockUnlock != null)
			{
				((ToolStripItem)_LockUnlock).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem UpDown
	{
		[DebuggerNonUserCode]
		get
		{
			return _UpDown;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = UpDown_Click;
			if (_UpDown != null)
			{
				((ToolStripItem)_UpDown).Click -= eventHandler;
			}
			_UpDown = value;
			if (_UpDown != null)
			{
				((ToolStripItem)_UpDown).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem ShiftMax
	{
		[DebuggerNonUserCode]
		get
		{
			return _ShiftMax;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = ShiftMax_Click;
			if (_ShiftMax != null)
			{
				((ToolStripItem)_ShiftMax).Click -= eventHandler;
			}
			_ShiftMax = value;
			if (_ShiftMax != null)
			{
				((ToolStripItem)_ShiftMax).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem ShiftAndLockMinSpreadsToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _ShiftAndLockMinSpreadsToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_ShiftAndLockMinSpreadsToolStripMenuItem = value;
		}
	}

	internal virtual ToolStripMenuItem MinShiftToDownshiftSpreadToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _MinShiftToDownshiftSpreadToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_MinShiftToDownshiftSpreadToolStripMenuItem = value;
		}
	}

	internal virtual ToolStripTextBox Shift_Spread
	{
		[DebuggerNonUserCode]
		get
		{
			return _Shift_Spread;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = Shift_Spread_Click;
			if (_Shift_Spread != null)
			{
				((ToolStripControlHost)_Shift_Spread).LostFocus -= eventHandler;
			}
			_Shift_Spread = value;
			if (_Shift_Spread != null)
			{
				((ToolStripControlHost)_Shift_Spread).LostFocus += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem MinLockToUnlockSpreadToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _MinLockToUnlockSpreadToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_MinLockToUnlockSpreadToolStripMenuItem = value;
		}
	}

	internal virtual ToolStripTextBox Lock_Spread
	{
		[DebuggerNonUserCode]
		get
		{
			return _Lock_Spread;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = Lock_Spread_Click;
			if (_Lock_Spread != null)
			{
				((ToolStripControlHost)_Lock_Spread).LostFocus -= eventHandler;
			}
			_Lock_Spread = value;
			if (_Lock_Spread != null)
			{
				((ToolStripControlHost)_Lock_Spread).LostFocus += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem Shift_Lock_Spread
	{
		[DebuggerNonUserCode]
		get
		{
			return _Shift_Lock_Spread;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Shift_Lock_Spread = value;
		}
	}

	internal virtual ToolStripTextBox Lock_Shift_Spread
	{
		[DebuggerNonUserCode]
		get
		{
			return _Lock_Shift_Spread;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = Lock_UpShift_Spread_Click;
			if (_Lock_Shift_Spread != null)
			{
				((ToolStripControlHost)_Lock_Shift_Spread).LostFocus -= eventHandler;
			}
			_Lock_Shift_Spread = value;
			if (_Lock_Shift_Spread != null)
			{
				((ToolStripControlHost)_Lock_Shift_Spread).LostFocus += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem ToolStripMenuItem1
	{
		[DebuggerNonUserCode]
		get
		{
			return _ToolStripMenuItem1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_ToolStripMenuItem1 = value;
		}
	}

	internal virtual ToolStripTextBox Unlock_Shift_Spread
	{
		[DebuggerNonUserCode]
		get
		{
			return _Unlock_Shift_Spread;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = Unlock_Downshift_Spread_Click;
			if (_Unlock_Shift_Spread != null)
			{
				((ToolStripControlHost)_Unlock_Shift_Spread).LostFocus -= eventHandler;
			}
			_Unlock_Shift_Spread = value;
			if (_Unlock_Shift_Spread != null)
			{
				((ToolStripControlHost)_Unlock_Shift_Spread).LostFocus += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem Metric
	{
		[DebuggerNonUserCode]
		get
		{
			return _Metric;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = Metric_Click;
			if (_Metric != null)
			{
				_Metric.CheckedChanged -= eventHandler;
			}
			_Metric = value;
			if (_Metric != null)
			{
				_Metric.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual OpenFileDialog OpenFileDialog1
	{
		[DebuggerNonUserCode]
		get
		{
			return _OpenFileDialog1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_OpenFileDialog1 = value;
		}
	}

	internal virtual SaveFileDialog SaveFileDialog1
	{
		[DebuggerNonUserCode]
		get
		{
			return _SaveFileDialog1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_SaveFileDialog1 = value;
		}
	}

	internal virtual ToolStripMenuItem DynoMode
	{
		[DebuggerNonUserCode]
		get
		{
			return _DynoMode;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = DynoMode_Click;
			if (_DynoMode != null)
			{
				((ToolStripItem)_DynoMode).Click -= eventHandler;
			}
			_DynoMode = value;
			if (_DynoMode != null)
			{
				((ToolStripItem)_DynoMode).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem LeadRpm
	{
		[DebuggerNonUserCode]
		get
		{
			return _LeadRpm;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = LeadRpm_Click;
			if (_LeadRpm != null)
			{
				((ToolStripItem)_LeadRpm).Click -= eventHandler;
			}
			_LeadRpm = value;
			if (_LeadRpm != null)
			{
				((ToolStripItem)_LeadRpm).Click += eventHandler;
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

	internal virtual ToolStripMenuItem No2CT_6L
	{
		[DebuggerNonUserCode]
		get
		{
			return _No2CT_6L;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = No2CT_6L_Click;
			if (_No2CT_6L != null)
			{
				((ToolStripItem)_No2CT_6L).Click -= eventHandler;
			}
			_No2CT_6L = value;
			if (_No2CT_6L != null)
			{
				((ToolStripItem)_No2CT_6L).Click += eventHandler;
			}
		}
	}

	internal virtual Button Lead_Button
	{
		[DebuggerNonUserCode]
		get
		{
			return _Lead_Button;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = Lead_Button_Click;
			if (_Lead_Button != null)
			{
				((Control)_Lead_Button).Click -= eventHandler;
			}
			_Lead_Button = value;
			if (_Lead_Button != null)
			{
				((Control)_Lead_Button).Click += eventHandler;
			}
		}
	}

	internal virtual Button TCC_Button
	{
		[DebuggerNonUserCode]
		get
		{
			return _TCC_Button;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = TCC_Button_Click;
			if (_TCC_Button != null)
			{
				((Control)_TCC_Button).Click -= eventHandler;
			}
			_TCC_Button = value;
			if (_TCC_Button != null)
			{
				((Control)_TCC_Button).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem MaxSpeed_Locked
	{
		[DebuggerNonUserCode]
		get
		{
			return _MaxSpeed_Locked;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = MaxSpeed_Locked_Click;
			if (_MaxSpeed_Locked != null)
			{
				((ToolStripItem)_MaxSpeed_Locked).Click -= eventHandler;
			}
			_MaxSpeed_Locked = value;
			if (_MaxSpeed_Locked != null)
			{
				((ToolStripItem)_MaxSpeed_Locked).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem ULckStay
	{
		[DebuggerNonUserCode]
		get
		{
			return _ULckStay;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = ULckStay_Click;
			if (_ULckStay != null)
			{
				((ToolStripItem)_ULckStay).Click -= eventHandler;
			}
			_ULckStay = value;
			if (_ULckStay != null)
			{
				((ToolStripItem)_ULckStay).Click += eventHandler;
			}
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

	internal virtual ToolStripMenuItem SGS
	{
		[DebuggerNonUserCode]
		get
		{
			return _SGS;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = SGS_Click;
			if (_SGS != null)
			{
				((ToolStripItem)_SGS).Click -= eventHandler;
			}
			_SGS = value;
			if (_SGS != null)
			{
				((ToolStripItem)_SGS).Click += eventHandler;
			}
		}
	}

	internal virtual NumericUpDown TireVisible
	{
		[DebuggerNonUserCode]
		get
		{
			return _TireVisible;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = TireVisible_ValueChanged;
			if (_TireVisible != null)
			{
				_TireVisible.ValueChanged -= eventHandler;
			}
			_TireVisible = value;
			if (_TireVisible != null)
			{
				_TireVisible.ValueChanged += eventHandler;
			}
		}
	}

	internal virtual CheckBox OverRide_Enable
	{
		[DebuggerNonUserCode]
		get
		{
			return _OverRide_Enable;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = OverRide_Enable_CheckedChanged;
			if (_OverRide_Enable != null)
			{
				_OverRide_Enable.CheckedChanged -= eventHandler;
			}
			_OverRide_Enable = value;
			if (_OverRide_Enable != null)
			{
				_OverRide_Enable.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual Button OverRide_Button
	{
		[DebuggerNonUserCode]
		get
		{
			return _OverRide_Button;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = OverRide_Button_Click;
			if (_OverRide_Button != null)
			{
				((Control)_OverRide_Button).Click -= eventHandler;
			}
			_OverRide_Button = value;
			if (_OverRide_Button != null)
			{
				((Control)_OverRide_Button).Click += eventHandler;
			}
		}
	}

	internal virtual Button OverRideReset_Button
	{
		[DebuggerNonUserCode]
		get
		{
			return _OverRideReset_Button;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = OverRideReset_Button_Click;
			if (_OverRideReset_Button != null)
			{
				((Control)_OverRideReset_Button).Click -= eventHandler;
			}
			_OverRideReset_Button = value;
			if (_OverRideReset_Button != null)
			{
				((Control)_OverRideReset_Button).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem HelpToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _HelpToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_HelpToolStripMenuItem = value;
		}
	}

	internal virtual ToolStripMenuItem AboutToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _AboutToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = AboutToolStripMenuItem_Click;
			if (_AboutToolStripMenuItem != null)
			{
				((ToolStripItem)_AboutToolStripMenuItem).Click -= eventHandler;
			}
			_AboutToolStripMenuItem = value;
			if (_AboutToolStripMenuItem != null)
			{
				((ToolStripItem)_AboutToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem RRM
	{
		[DebuggerNonUserCode]
		get
		{
			return _RRM;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = RRM_Click;
			if (_RRM != null)
			{
				((ToolStripItem)_RRM).Click -= eventHandler;
			}
			_RRM = value;
			if (_RRM != null)
			{
				((ToolStripItem)_RRM).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem WOTTCCPrep
	{
		[DebuggerNonUserCode]
		get
		{
			return _WOTTCCPrep;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = WOTTCCPrep_Click;
			if (_WOTTCCPrep != null)
			{
				((ToolStripItem)_WOTTCCPrep).Click -= eventHandler;
			}
			_WOTTCCPrep = value;
			if (_WOTTCCPrep != null)
			{
				((ToolStripItem)_WOTTCCPrep).Click += eventHandler;
			}
		}
	}

	internal virtual Button TireCalc
	{
		[DebuggerNonUserCode]
		get
		{
			return _TireCalc;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = TireCalc_Click;
			if (_TireCalc != null)
			{
				((Control)_TireCalc).Click -= eventHandler;
			}
			_TireCalc = value;
			if (_TireCalc != null)
			{
				((Control)_TireCalc).Click += eventHandler;
			}
		}
	}

	public Main_Form()
	{
		((Form)this).Load += Main_Form_Load;
		((Form)this).Shown += Main_Form_Shown;
		Stall_Slip = 0f;
		MinSpeed = new float[13];
		MinTCCSpeed = new float[19, 13];
		StallBase = new float[17]
		{
			0f, 0f, 0.05f, 0.1f, 0.2f, 0.3f, 0.4f, 0.5f, 0.55f, 0.6f,
			0.65f, 0.7f, 0.75f, 0.8f, 0.9f, 1f, 1f
		};
		StallMin = new object[19];
		Dis_High = 255;
		Dis_Low = 254;
		Init = 0;
		US = 0;
		PDC = 0uL;
		D_SC = 0;
		TransPresets = new List<Trans_Preset>();
		SlopePresets = new List<Slope_Preset>();
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
		//IL_0053: Unknown result type (might be due to invalid IL or missing references)
		//IL_005d: Expected O, but got Unknown
		//IL_005e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0068: Expected O, but got Unknown
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
		//IL_00c1: Unknown result type (might be due to invalid IL or missing references)
		//IL_00cb: Expected O, but got Unknown
		//IL_00cc: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d6: Expected O, but got Unknown
		//IL_00d7: Unknown result type (might be due to invalid IL or missing references)
		//IL_00e1: Expected O, but got Unknown
		//IL_00e2: Unknown result type (might be due to invalid IL or missing references)
		//IL_00ec: Expected O, but got Unknown
		//IL_00ed: Unknown result type (might be due to invalid IL or missing references)
		//IL_00f7: Expected O, but got Unknown
		//IL_00f8: Unknown result type (might be due to invalid IL or missing references)
		//IL_0102: Expected O, but got Unknown
		//IL_0103: Unknown result type (might be due to invalid IL or missing references)
		//IL_010d: Expected O, but got Unknown
		//IL_010e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0118: Expected O, but got Unknown
		//IL_0119: Unknown result type (might be due to invalid IL or missing references)
		//IL_0123: Expected O, but got Unknown
		//IL_0124: Unknown result type (might be due to invalid IL or missing references)
		//IL_012e: Expected O, but got Unknown
		//IL_012f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0139: Expected O, but got Unknown
		//IL_013a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0144: Expected O, but got Unknown
		//IL_0145: Unknown result type (might be due to invalid IL or missing references)
		//IL_014f: Expected O, but got Unknown
		//IL_0150: Unknown result type (might be due to invalid IL or missing references)
		//IL_015a: Expected O, but got Unknown
		//IL_015b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0165: Expected O, but got Unknown
		//IL_0166: Unknown result type (might be due to invalid IL or missing references)
		//IL_0170: Expected O, but got Unknown
		//IL_0171: Unknown result type (might be due to invalid IL or missing references)
		//IL_017b: Expected O, but got Unknown
		//IL_0187: Unknown result type (might be due to invalid IL or missing references)
		//IL_0191: Expected O, but got Unknown
		//IL_0192: Unknown result type (might be due to invalid IL or missing references)
		//IL_019c: Expected O, but got Unknown
		//IL_019d: Unknown result type (might be due to invalid IL or missing references)
		//IL_01a7: Expected O, but got Unknown
		//IL_01a8: Unknown result type (might be due to invalid IL or missing references)
		//IL_01b2: Expected O, but got Unknown
		//IL_01b3: Unknown result type (might be due to invalid IL or missing references)
		//IL_01bd: Expected O, but got Unknown
		//IL_01be: Unknown result type (might be due to invalid IL or missing references)
		//IL_01c8: Expected O, but got Unknown
		//IL_01c9: Unknown result type (might be due to invalid IL or missing references)
		//IL_01d3: Expected O, but got Unknown
		//IL_01d4: Unknown result type (might be due to invalid IL or missing references)
		//IL_01de: Expected O, but got Unknown
		//IL_01df: Unknown result type (might be due to invalid IL or missing references)
		//IL_01e9: Expected O, but got Unknown
		//IL_01ea: Unknown result type (might be due to invalid IL or missing references)
		//IL_01f4: Expected O, but got Unknown
		//IL_01f5: Unknown result type (might be due to invalid IL or missing references)
		//IL_01ff: Expected O, but got Unknown
		//IL_0200: Unknown result type (might be due to invalid IL or missing references)
		//IL_020a: Expected O, but got Unknown
		//IL_020b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0215: Expected O, but got Unknown
		//IL_0216: Unknown result type (might be due to invalid IL or missing references)
		//IL_0220: Expected O, but got Unknown
		//IL_0221: Unknown result type (might be due to invalid IL or missing references)
		//IL_022b: Expected O, but got Unknown
		//IL_022c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0236: Expected O, but got Unknown
		//IL_0237: Unknown result type (might be due to invalid IL or missing references)
		//IL_0241: Expected O, but got Unknown
		//IL_024d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0257: Expected O, but got Unknown
		//IL_0258: Unknown result type (might be due to invalid IL or missing references)
		//IL_0262: Expected O, but got Unknown
		//IL_0263: Unknown result type (might be due to invalid IL or missing references)
		//IL_026d: Expected O, but got Unknown
		//IL_026e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0278: Expected O, but got Unknown
		//IL_0279: Unknown result type (might be due to invalid IL or missing references)
		//IL_0283: Expected O, but got Unknown
		//IL_0284: Unknown result type (might be due to invalid IL or missing references)
		//IL_028e: Expected O, but got Unknown
		//IL_028f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0299: Expected O, but got Unknown
		//IL_029a: Unknown result type (might be due to invalid IL or missing references)
		//IL_02a4: Expected O, but got Unknown
		//IL_02a5: Unknown result type (might be due to invalid IL or missing references)
		//IL_02af: Expected O, but got Unknown
		//IL_02b0: Unknown result type (might be due to invalid IL or missing references)
		//IL_02ba: Expected O, but got Unknown
		//IL_02c1: Unknown result type (might be due to invalid IL or missing references)
		//IL_02cb: Expected O, but got Unknown
		//IL_02cc: Unknown result type (might be due to invalid IL or missing references)
		//IL_02d6: Expected O, but got Unknown
		//IL_02d7: Unknown result type (might be due to invalid IL or missing references)
		//IL_02e1: Expected O, but got Unknown
		//IL_02e2: Unknown result type (might be due to invalid IL or missing references)
		//IL_02ec: Expected O, but got Unknown
		//IL_02ed: Unknown result type (might be due to invalid IL or missing references)
		//IL_02f7: Expected O, but got Unknown
		//IL_02f8: Unknown result type (might be due to invalid IL or missing references)
		//IL_0302: Expected O, but got Unknown
		//IL_0303: Unknown result type (might be due to invalid IL or missing references)
		//IL_030d: Expected O, but got Unknown
		//IL_030e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0318: Expected O, but got Unknown
		//IL_0319: Unknown result type (might be due to invalid IL or missing references)
		//IL_0323: Expected O, but got Unknown
		//IL_0324: Unknown result type (might be due to invalid IL or missing references)
		//IL_032e: Expected O, but got Unknown
		//IL_032f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0339: Expected O, but got Unknown
		//IL_033a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0344: Expected O, but got Unknown
		//IL_0345: Unknown result type (might be due to invalid IL or missing references)
		//IL_034f: Expected O, but got Unknown
		//IL_0350: Unknown result type (might be due to invalid IL or missing references)
		//IL_035a: Expected O, but got Unknown
		//IL_035b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0365: Expected O, but got Unknown
		//IL_0366: Unknown result type (might be due to invalid IL or missing references)
		//IL_0370: Expected O, but got Unknown
		//IL_0371: Unknown result type (might be due to invalid IL or missing references)
		//IL_037b: Expected O, but got Unknown
		//IL_037c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0386: Expected O, but got Unknown
		//IL_0387: Unknown result type (might be due to invalid IL or missing references)
		//IL_0391: Expected O, but got Unknown
		//IL_0392: Unknown result type (might be due to invalid IL or missing references)
		//IL_039c: Expected O, but got Unknown
		//IL_039d: Unknown result type (might be due to invalid IL or missing references)
		//IL_03a7: Expected O, but got Unknown
		//IL_03a8: Unknown result type (might be due to invalid IL or missing references)
		//IL_03b2: Expected O, but got Unknown
		//IL_03b3: Unknown result type (might be due to invalid IL or missing references)
		//IL_03bd: Expected O, but got Unknown
		//IL_03be: Unknown result type (might be due to invalid IL or missing references)
		//IL_03c8: Expected O, but got Unknown
		//IL_03c9: Unknown result type (might be due to invalid IL or missing references)
		//IL_03d3: Expected O, but got Unknown
		//IL_03d4: Unknown result type (might be due to invalid IL or missing references)
		//IL_03de: Expected O, but got Unknown
		//IL_03df: Unknown result type (might be due to invalid IL or missing references)
		//IL_03e9: Expected O, but got Unknown
		//IL_03ea: Unknown result type (might be due to invalid IL or missing references)
		//IL_03f4: Expected O, but got Unknown
		//IL_03f5: Unknown result type (might be due to invalid IL or missing references)
		//IL_03ff: Expected O, but got Unknown
		//IL_0400: Unknown result type (might be due to invalid IL or missing references)
		//IL_040a: Expected O, but got Unknown
		//IL_040b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0415: Expected O, but got Unknown
		//IL_0416: Unknown result type (might be due to invalid IL or missing references)
		//IL_0420: Expected O, but got Unknown
		//IL_0421: Unknown result type (might be due to invalid IL or missing references)
		//IL_042b: Expected O, but got Unknown
		//IL_042c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0436: Expected O, but got Unknown
		//IL_0437: Unknown result type (might be due to invalid IL or missing references)
		//IL_0441: Expected O, but got Unknown
		//IL_0442: Unknown result type (might be due to invalid IL or missing references)
		//IL_044c: Expected O, but got Unknown
		//IL_044d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0457: Expected O, but got Unknown
		//IL_0458: Unknown result type (might be due to invalid IL or missing references)
		//IL_0462: Expected O, but got Unknown
		//IL_0463: Unknown result type (might be due to invalid IL or missing references)
		//IL_046d: Expected O, but got Unknown
		//IL_0474: Unknown result type (might be due to invalid IL or missing references)
		//IL_047e: Expected O, but got Unknown
		//IL_047f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0489: Expected O, but got Unknown
		//IL_0592: Unknown result type (might be due to invalid IL or missing references)
		//IL_059c: Expected O, but got Unknown
		//IL_07a2: Unknown result type (might be due to invalid IL or missing references)
		//IL_07ac: Expected O, but got Unknown
		//IL_09a2: Unknown result type (might be due to invalid IL or missing references)
		//IL_09ac: Expected O, but got Unknown
		//IL_0bb2: Unknown result type (might be due to invalid IL or missing references)
		//IL_0bbc: Expected O, but got Unknown
		//IL_0dc5: Unknown result type (might be due to invalid IL or missing references)
		//IL_0dcf: Expected O, but got Unknown
		//IL_1122: Unknown result type (might be due to invalid IL or missing references)
		//IL_112c: Expected O, but got Unknown
		//IL_1747: Unknown result type (might be due to invalid IL or missing references)
		//IL_1751: Expected O, but got Unknown
		//IL_24ce: Unknown result type (might be due to invalid IL or missing references)
		//IL_24d8: Expected O, but got Unknown
		//IL_32ee: Unknown result type (might be due to invalid IL or missing references)
		//IL_32f8: Expected O, but got Unknown
		//IL_4bff: Unknown result type (might be due to invalid IL or missing references)
		//IL_4c09: Expected O, but got Unknown
		components = new Container();
		ComponentResourceManager componentResourceManager = new ComponentResourceManager(typeof(Main_Form));
		U_Shift = new BCGridControl();
		BcGridControl1 = new BCGridControl();
		D_Shift = new BCGridControl();
		Lock = new BCGridControl();
		Unlock = new BCGridControl();
		Gears = new NumericUpDown();
		Label1 = new Label();
		Slope = new BCGridControl();
		GroupBox1 = new GroupBox();
		GroupBox2 = new GroupBox();
		Lead_Button = new Button();
		Label17 = new Label();
		VSS = new NumericUpDown();
		Label9 = new Label();
		Ratio = new BCGridControl();
		ComboBox1 = new ComboBox();
		GroupBox3 = new GroupBox();
		OverRide_Enable = new CheckBox();
		Label8 = new Label();
		Label7 = new Label();
		Label6 = new Label();
		Label4 = new Label();
		UpF = new NumericUpDown();
		Label5 = new Label();
		DownF = new NumericUpDown();
		Label3 = new Label();
		Offset = new NumericUpDown();
		Label2 = new Label();
		Factor = new NumericUpDown();
		ComboBox2 = new ComboBox();
		OverRide_Button = new Button();
		OverRideReset_Button = new Button();
		Speed = new BCGridControl();
		GroupBox4 = new GroupBox();
		Label13 = new Label();
		Label12 = new Label();
		Label11 = new Label();
		Label10 = new Label();
		GroupBox5 = new GroupBox();
		TireCalc = new Button();
		TireVisible = new NumericUpDown();
		Label21 = new Label();
		DRPM = new NumericUpDown();
		Label20 = new Label();
		Idle = new NumericUpDown();
		Label16 = new Label();
		Tire = new NumericUpDown();
		Label15 = new Label();
		Gear = new NumericUpDown();
		Label14 = new Label();
		RPM = new BCGridControl();
		GroupBox6 = new GroupBox();
		TCC_Button = new Button();
		Label25 = new Label();
		WotLck = new NumericUpDown();
		Label24 = new Label();
		AclLck = new NumericUpDown();
		Label23 = new Label();
		MinLck = new NumericUpDown();
		Label18 = new Label();
		Stall = new NumericUpDown();
		Timer1 = new Timer(components);
		MenuStrip1 = new MenuStrip();
		FileToolStripMenuItem = new ToolStripMenuItem();
		OpenToolStripMenuItem = new ToolStripMenuItem();
		SaveToolStripMenuItem = new ToolStripMenuItem();
		ExportToolStripMenuItem = new ToolStripMenuItem();
		ExportWindowToolStripMenuItem = new ToolStripMenuItem();
		OptionsToolStripMenuItem = new ToolStripMenuItem();
		Metric = new ToolStripMenuItem();
		DynoMode = new ToolStripMenuItem();
		RRM = new ToolStripMenuItem();
		SGS = new ToolStripMenuItem();
		StallLogic = new ToolStripMenuItem();
		MaxSpeed_Locked = new ToolStripMenuItem();
		ULckStay = new ToolStripMenuItem();
		LeadRpm = new ToolStripMenuItem();
		Allow4L60WOT4th = new ToolStripMenuItem();
		WOTTCCPrep = new ToolStripMenuItem();
		No2CT_6L = new ToolStripMenuItem();
		LogicChecksRulesToolStripMenuItem = new ToolStripMenuItem();
		InitLock = new ToolStripMenuItem();
		PreLock = new ToolStripMenuItem();
		PostLock = new ToolStripMenuItem();
		LockUnlock = new ToolStripMenuItem();
		UpDown = new ToolStripMenuItem();
		ShiftMax = new ToolStripMenuItem();
		ShiftAndLockMinSpreadsToolStripMenuItem = new ToolStripMenuItem();
		MinShiftToDownshiftSpreadToolStripMenuItem = new ToolStripMenuItem();
		Shift_Spread = new ToolStripTextBox();
		MinLockToUnlockSpreadToolStripMenuItem = new ToolStripMenuItem();
		Lock_Spread = new ToolStripTextBox();
		Shift_Lock_Spread = new ToolStripMenuItem();
		Lock_Shift_Spread = new ToolStripTextBox();
		ToolStripMenuItem1 = new ToolStripMenuItem();
		Unlock_Shift_Spread = new ToolStripTextBox();
		HelpToolStripMenuItem = new ToolStripMenuItem();
		AboutToolStripMenuItem = new ToolStripMenuItem();
		OpenFileDialog1 = new OpenFileDialog();
		SaveFileDialog1 = new SaveFileDialog();
		ToolTip1 = new ToolTip(components);
		Label19 = new Label();
		((ISupportInitialize)Gears).BeginInit();
		((Control)GroupBox1).SuspendLayout();
		((Control)GroupBox2).SuspendLayout();
		((ISupportInitialize)VSS).BeginInit();
		((Control)GroupBox3).SuspendLayout();
		((ISupportInitialize)UpF).BeginInit();
		((ISupportInitialize)DownF).BeginInit();
		((ISupportInitialize)Offset).BeginInit();
		((ISupportInitialize)Factor).BeginInit();
		((Control)GroupBox4).SuspendLayout();
		((Control)GroupBox5).SuspendLayout();
		((ISupportInitialize)TireVisible).BeginInit();
		((ISupportInitialize)DRPM).BeginInit();
		((ISupportInitialize)Idle).BeginInit();
		((ISupportInitialize)Tire).BeginInit();
		((ISupportInitialize)Gear).BeginInit();
		((Control)GroupBox6).SuspendLayout();
		((ISupportInitialize)WotLck).BeginInit();
		((ISupportInitialize)AclLck).BeginInit();
		((ISupportInitialize)MinLck).BeginInit();
		((ISupportInitialize)Stall).BeginInit();
		((Control)MenuStrip1).SuspendLayout();
		((Control)this).SuspendLayout();
		((Control)U_Shift).BackgroundImage = (Image)componentResourceManager.GetObject("U_Shift.BackgroundImage");
		((Control)U_Shift).BackgroundImageLayout = (ImageLayout)0;
		U_Shift.Cell_Auto_W = 0;
		U_Shift.Cell_CharMax = 5;
		U_Shift.Cell_CPFormat = "##0.###";
		U_Shift.Cell_FontCLR = Color.Black;
		U_Shift.Cell_Format = "##0";
		U_Shift.Cell_FSelCLR = Color.White;
		U_Shift.Cell_H = 12;
		U_Shift.Cell_HighCLR = Color.RoyalBlue;
		U_Shift.Cell_HSelCLR = Color.DarkRed;
		U_Shift.Cell_LabelFormat = "##0";
		U_Shift.Cell_LowCLR = Color.White;
		U_Shift.Cell_LSelCLR = Color.Red;
		U_Shift.Cell_ShowChanges = 0;
		U_Shift.Cell_W = 32;
		U_Shift.Grid_AxisStatus = 0;
		U_Shift.Grid_DataOffset = 0f;
		U_Shift.Grid_DataScalar = 1f;
		U_Shift.Grid_DataSCopyPaste = 1;
		U_Shift.Grid_DataStatus = 3997;
		U_Shift.Grid_FreezeDraw = 0;
		U_Shift.Grid_GraphType = 1;
		U_Shift.Grid_ReDraw = 0;
		U_Shift.Grid_ShowLabels = 1;
		U_Shift.Grid_Transpose = 0;
		U_Shift.Grid_TransposeCopyPaste = 0;
		U_Shift.Grid_VisibleName = "Upshift";
		U_Shift.Grid_X = 17;
		U_Shift.Grid_Y = 3;
		BCGridControl u_Shift = U_Shift;
		Point location = new Point(6, 19);
		((Control)u_Shift).Location = location;
		((Control)U_Shift).Name = "U_Shift";
		BCGridControl u_Shift2 = U_Shift;
		Size size = new Size(577, 49);
		((Control)u_Shift2).Size = size;
		((Control)U_Shift).TabIndex = 0;
		ToolTip1.SetToolTip((Control)(object)U_Shift, "Upshit Speeds");
		((Control)BcGridControl1).BackgroundImage = (Image)componentResourceManager.GetObject("BcGridControl1.BackgroundImage");
		((Control)BcGridControl1).BackgroundImageLayout = (ImageLayout)0;
		BcGridControl1.Cell_Auto_W = 0;
		BcGridControl1.Cell_CharMax = 5;
		BcGridControl1.Cell_CPFormat = "###,###,###,##0.############";
		BcGridControl1.Cell_FontCLR = Color.Black;
		BcGridControl1.Cell_Format = "##0.0";
		BcGridControl1.Cell_FSelCLR = Color.White;
		BcGridControl1.Cell_H = 12;
		BcGridControl1.Cell_HighCLR = Color.RoyalBlue;
		BcGridControl1.Cell_HSelCLR = Color.DarkRed;
		BcGridControl1.Cell_LabelFormat = "####0";
		BcGridControl1.Cell_LowCLR = Color.White;
		BcGridControl1.Cell_LSelCLR = Color.Red;
		BcGridControl1.Cell_ShowChanges = 0;
		BcGridControl1.Cell_W = 32;
		BcGridControl1.Grid_AxisStatus = 0;
		BcGridControl1.Grid_DataOffset = 0f;
		BcGridControl1.Grid_DataScalar = 1f;
		BcGridControl1.Grid_DataSCopyPaste = 1;
		BcGridControl1.Grid_DataStatus = 878;
		BcGridControl1.Grid_FreezeDraw = 0;
		BcGridControl1.Grid_GraphType = 1;
		BcGridControl1.Grid_ReDraw = 0;
		BcGridControl1.Grid_ShowLabels = 0;
		BcGridControl1.Grid_Transpose = 0;
		BcGridControl1.Grid_TransposeCopyPaste = 0;
		BcGridControl1.Grid_VisibleName = "BCGridControl";
		BcGridControl1.Grid_X = 4;
		BcGridControl1.Grid_Y = 4;
		BCGridControl bcGridControl = BcGridControl1;
		location = new Point(1010, 503);
		((Control)bcGridControl).Location = location;
		((Control)BcGridControl1).Name = "BcGridControl1";
		BCGridControl bcGridControl2 = BcGridControl1;
		size = new Size(129, 49);
		((Control)bcGridControl2).Size = size;
		((Control)BcGridControl1).TabIndex = 1;
		((Control)D_Shift).BackgroundImage = (Image)componentResourceManager.GetObject("D_Shift.BackgroundImage");
		((Control)D_Shift).BackgroundImageLayout = (ImageLayout)0;
		D_Shift.Cell_Auto_W = 0;
		D_Shift.Cell_CharMax = 5;
		D_Shift.Cell_CPFormat = "##0.###";
		D_Shift.Cell_FontCLR = Color.Black;
		D_Shift.Cell_Format = "##0";
		D_Shift.Cell_FSelCLR = Color.White;
		D_Shift.Cell_H = 12;
		D_Shift.Cell_HighCLR = Color.RoyalBlue;
		D_Shift.Cell_HSelCLR = Color.DarkRed;
		D_Shift.Cell_LabelFormat = "##0";
		D_Shift.Cell_LowCLR = Color.White;
		D_Shift.Cell_LSelCLR = Color.Red;
		D_Shift.Cell_ShowChanges = 0;
		D_Shift.Cell_W = 32;
		D_Shift.Grid_AxisStatus = 0;
		D_Shift.Grid_DataOffset = 0f;
		D_Shift.Grid_DataScalar = 1f;
		D_Shift.Grid_DataSCopyPaste = 1;
		D_Shift.Grid_DataStatus = 3243;
		D_Shift.Grid_FreezeDraw = 0;
		D_Shift.Grid_GraphType = 1;
		D_Shift.Grid_ReDraw = 0;
		D_Shift.Grid_ShowLabels = 1;
		D_Shift.Grid_Transpose = 0;
		D_Shift.Grid_TransposeCopyPaste = 0;
		D_Shift.Grid_VisibleName = "Down Shift";
		D_Shift.Grid_X = 17;
		D_Shift.Grid_Y = 3;
		BCGridControl d_Shift = D_Shift;
		location = new Point(6, 74);
		((Control)d_Shift).Location = location;
		((Control)D_Shift).Name = "D_Shift";
		BCGridControl d_Shift2 = D_Shift;
		size = new Size(577, 49);
		((Control)d_Shift2).Size = size;
		((Control)D_Shift).TabIndex = 2;
		ToolTip1.SetToolTip((Control)(object)D_Shift, "Downshift Speeds");
		((Control)Lock).BackgroundImage = (Image)componentResourceManager.GetObject("Lock.BackgroundImage");
		((Control)Lock).BackgroundImageLayout = (ImageLayout)0;
		Lock.Cell_Auto_W = 0;
		Lock.Cell_CharMax = 5;
		Lock.Cell_CPFormat = "##0.###";
		Lock.Cell_FontCLR = Color.Black;
		Lock.Cell_Format = "##0";
		Lock.Cell_FSelCLR = Color.White;
		Lock.Cell_H = 12;
		Lock.Cell_HighCLR = Color.RoyalBlue;
		Lock.Cell_HSelCLR = Color.DarkRed;
		Lock.Cell_LabelFormat = "##0";
		Lock.Cell_LowCLR = Color.White;
		Lock.Cell_LSelCLR = Color.Red;
		Lock.Cell_ShowChanges = 0;
		Lock.Cell_W = 32;
		Lock.Grid_AxisStatus = 0;
		Lock.Grid_DataOffset = 0f;
		Lock.Grid_DataScalar = 1f;
		Lock.Grid_DataSCopyPaste = 1;
		Lock.Grid_DataStatus = 2653;
		Lock.Grid_FreezeDraw = 0;
		Lock.Grid_GraphType = 1;
		Lock.Grid_ReDraw = 0;
		Lock.Grid_ShowLabels = 1;
		Lock.Grid_Transpose = 0;
		Lock.Grid_TransposeCopyPaste = 0;
		Lock.Grid_VisibleName = "Lock";
		Lock.Grid_X = 17;
		Lock.Grid_Y = 3;
		BCGridControl bCGridControl = Lock;
		location = new Point(6, 129);
		((Control)bCGridControl).Location = location;
		((Control)Lock).Name = "Lock";
		BCGridControl bCGridControl2 = Lock;
		size = new Size(577, 49);
		((Control)bCGridControl2).Size = size;
		((Control)Lock).TabIndex = 3;
		ToolTip1.SetToolTip((Control)(object)Lock, "Lockup Speeds");
		((Control)Unlock).BackgroundImage = (Image)componentResourceManager.GetObject("Unlock.BackgroundImage");
		((Control)Unlock).BackgroundImageLayout = (ImageLayout)0;
		Unlock.Cell_Auto_W = 0;
		Unlock.Cell_CharMax = 5;
		Unlock.Cell_CPFormat = "##0.###";
		Unlock.Cell_FontCLR = Color.Black;
		Unlock.Cell_Format = "##0";
		Unlock.Cell_FSelCLR = Color.White;
		Unlock.Cell_H = 12;
		Unlock.Cell_HighCLR = Color.RoyalBlue;
		Unlock.Cell_HSelCLR = Color.DarkRed;
		Unlock.Cell_LabelFormat = "##0";
		Unlock.Cell_LowCLR = Color.White;
		Unlock.Cell_LSelCLR = Color.Red;
		Unlock.Cell_ShowChanges = 0;
		Unlock.Cell_W = 32;
		Unlock.Grid_AxisStatus = 0;
		Unlock.Grid_DataOffset = 0f;
		Unlock.Grid_DataScalar = 1f;
		Unlock.Grid_DataSCopyPaste = 1;
		Unlock.Grid_DataStatus = 2459;
		Unlock.Grid_FreezeDraw = 0;
		Unlock.Grid_GraphType = 1;
		Unlock.Grid_ReDraw = 0;
		Unlock.Grid_ShowLabels = 1;
		Unlock.Grid_Transpose = 0;
		Unlock.Grid_TransposeCopyPaste = 0;
		Unlock.Grid_VisibleName = "Unlock";
		Unlock.Grid_X = 17;
		Unlock.Grid_Y = 3;
		BCGridControl unlock = Unlock;
		location = new Point(6, 184);
		((Control)unlock).Location = location;
		((Control)Unlock).Name = "Unlock";
		BCGridControl unlock2 = Unlock;
		size = new Size(577, 49);
		((Control)unlock2).Size = size;
		((Control)Unlock).TabIndex = 4;
		ToolTip1.SetToolTip((Control)(object)Unlock, "Unlock Speeds");
		NumericUpDown gears = Gears;
		location = new Point(49, 43);
		((Control)gears).Location = location;
		NumericUpDown gears2 = Gears;
		decimal maximum = new decimal(new int[4] { 12, 0, 0, 0 });
		gears2.Maximum = maximum;
		maximum = (Gears.Minimum = new decimal(new int[4] { 2, 0, 0, 0 }));
		((Control)Gears).Name = "Gears";
		NumericUpDown gears3 = Gears;
		size = new Size(32, 20);
		((Control)gears3).Size = size;
		((Control)Gears).TabIndex = 5;
		maximum = (Gears.Value = new decimal(new int[4] { 5, 0, 0, 0 }));
		Label1.AutoSize = true;
		Label label = Label1;
		location = new Point(8, 45);
		((Control)label).Location = location;
		((Control)Label1).Name = "Label1";
		Label label2 = Label1;
		size = new Size(35, 13);
		((Control)label2).Size = size;
		((Control)Label1).TabIndex = 6;
		Label1.Text = "Gears";
		ToolTip1.SetToolTip((Control)(object)Label1, "Number of forward gears in transmission.");
		((Control)Slope).BackgroundImage = (Image)componentResourceManager.GetObject("Slope.BackgroundImage");
		((Control)Slope).BackgroundImageLayout = (ImageLayout)0;
		Slope.Cell_Auto_W = 0;
		Slope.Cell_CharMax = 5;
		Slope.Cell_CPFormat = "##0.###";
		Slope.Cell_FontCLR = Color.Black;
		Slope.Cell_Format = "0.00";
		Slope.Cell_FSelCLR = Color.White;
		Slope.Cell_H = 12;
		Slope.Cell_HighCLR = Color.RoyalBlue;
		Slope.Cell_HSelCLR = Color.DarkRed;
		Slope.Cell_LabelFormat = "##0";
		Slope.Cell_LowCLR = Color.White;
		Slope.Cell_LSelCLR = Color.Red;
		Slope.Cell_ShowChanges = 0;
		Slope.Cell_W = 32;
		Slope.Grid_AxisStatus = 0;
		Slope.Grid_DataOffset = 0f;
		Slope.Grid_DataScalar = 1f;
		Slope.Grid_DataSCopyPaste = 1;
		Slope.Grid_DataStatus = 4341;
		Slope.Grid_FreezeDraw = 0;
		Slope.Grid_GraphType = 1;
		Slope.Grid_ReDraw = 0;
		Slope.Grid_ShowLabels = 0;
		Slope.Grid_Transpose = 0;
		Slope.Grid_TransposeCopyPaste = 0;
		Slope.Grid_VisibleName = "Base Shift Slopes";
		Slope.Grid_X = 17;
		Slope.Grid_Y = 3;
		BCGridControl slope = Slope;
		location = new Point(38, 46);
		((Control)slope).Location = location;
		((Control)Slope).Name = "Slope";
		BCGridControl slope2 = Slope;
		size = new Size(545, 37);
		((Control)slope2).Size = size;
		((Control)Slope).TabIndex = 7;
		ToolTip1.SetToolTip((Control)(object)Slope, "Shift Slopes");
		((Control)GroupBox1).Controls.Add((Control)(object)U_Shift);
		((Control)GroupBox1).Controls.Add((Control)(object)D_Shift);
		((Control)GroupBox1).Controls.Add((Control)(object)Lock);
		((Control)GroupBox1).Controls.Add((Control)(object)Unlock);
		GroupBox groupBox = GroupBox1;
		location = new Point(11, 253);
		((Control)groupBox).Location = location;
		((Control)GroupBox1).Name = "GroupBox1";
		GroupBox groupBox2 = GroupBox1;
		size = new Size(595, 247);
		((Control)groupBox2).Size = size;
		((Control)GroupBox1).TabIndex = 8;
		GroupBox1.TabStop = false;
		GroupBox1.Text = "Shift / Lockup Data";
		((Control)GroupBox2).Controls.Add((Control)(object)Lead_Button);
		((Control)GroupBox2).Controls.Add((Control)(object)Label17);
		((Control)GroupBox2).Controls.Add((Control)(object)VSS);
		((Control)GroupBox2).Controls.Add((Control)(object)Label9);
		((Control)GroupBox2).Controls.Add((Control)(object)Ratio);
		((Control)GroupBox2).Controls.Add((Control)(object)ComboBox1);
		((Control)GroupBox2).Controls.Add((Control)(object)Label1);
		((Control)GroupBox2).Controls.Add((Control)(object)Gears);
		GroupBox groupBox3 = GroupBox2;
		location = new Point(12, 27);
		((Control)groupBox3).Location = location;
		((Control)GroupBox2).Name = "GroupBox2";
		GroupBox groupBox4 = GroupBox2;
		size = new Size(160, 120);
		((Control)groupBox4).Size = size;
		((Control)GroupBox2).TabIndex = 9;
		GroupBox2.TabStop = false;
		GroupBox2.Text = "Transmission";
		Button lead_Button = Lead_Button;
		location = new Point(6, 90);
		((Control)lead_Button).Location = location;
		((Control)Lead_Button).Name = "Lead_Button";
		Button lead_Button2 = Lead_Button;
		size = new Size(109, 24);
		((Control)lead_Button2).Size = size;
		((Control)Lead_Button).TabIndex = 14;
		((ButtonBase)Lead_Button).Text = "Shift Lead Time";
		ToolTip1.SetToolTip((Control)(object)Lead_Button, "Shift lead time form.");
		((ButtonBase)Lead_Button).UseVisualStyleBackColor = true;
		Label17.AutoSize = true;
		Label label3 = Label17;
		location = new Point(8, 66);
		((Control)label3).Location = location;
		((Control)Label17).Name = "Label17";
		Label label4 = Label17;
		size = new Size(28, 13);
		((Control)label4).Size = size;
		((Control)Label17).TabIndex = 11;
		Label17.Text = "VSS";
		ToolTip1.SetToolTip((Control)(object)Label17, "Number of teeth/pulses of the vehicle speed sensor fitted in the transmission.");
		NumericUpDown vSS = VSS;
		location = new Point(49, 64);
		((Control)vSS).Location = location;
		maximum = (VSS.Maximum = new decimal(new int[4] { 200, 0, 0, 0 }));
		maximum = (VSS.Minimum = new decimal(new int[4] { 1, 0, 0, 0 }));
		((Control)VSS).Name = "VSS";
		NumericUpDown vSS2 = VSS;
		size = new Size(41, 20);
		((Control)vSS2).Size = size;
		((Control)VSS).TabIndex = 10;
		maximum = (VSS.Value = new decimal(new int[4] { 40, 0, 0, 0 }));
		Label9.AutoSize = true;
		Label label5 = Label9;
		location = new Point(122, 19);
		((Control)label5).Location = location;
		((Control)Label9).Name = "Label9";
		Label label6 = Label9;
		size = new Size(32, 13);
		((Control)label6).Size = size;
		((Control)Label9).TabIndex = 9;
		Label9.Text = "Ratio";
		((Control)Ratio).BackgroundImage = (Image)componentResourceManager.GetObject("Ratio.BackgroundImage");
		((Control)Ratio).BackgroundImageLayout = (ImageLayout)0;
		Ratio.Cell_Auto_W = 0;
		Ratio.Cell_CharMax = 5;
		Ratio.Cell_CPFormat = "###,###,###,##0.############";
		Ratio.Cell_FontCLR = Color.Black;
		Ratio.Cell_Format = "0.000";
		Ratio.Cell_FSelCLR = Color.White;
		Ratio.Cell_H = 12;
		Ratio.Cell_HighCLR = Color.White;
		Ratio.Cell_HSelCLR = Color.DarkRed;
		Ratio.Cell_LabelFormat = "####0";
		Ratio.Cell_LowCLR = Color.White;
		Ratio.Cell_LSelCLR = Color.Red;
		Ratio.Cell_ShowChanges = 0;
		Ratio.Cell_W = 32;
		Ratio.Grid_AxisStatus = 0;
		Ratio.Grid_DataOffset = 0f;
		Ratio.Grid_DataScalar = 1f;
		Ratio.Grid_DataSCopyPaste = 1;
		Ratio.Grid_DataStatus = 689;
		Ratio.Grid_FreezeDraw = 0;
		Ratio.Grid_GraphType = 0;
		Ratio.Grid_ReDraw = 0;
		Ratio.Grid_ShowLabels = 0;
		Ratio.Grid_Transpose = 0;
		Ratio.Grid_TransposeCopyPaste = 0;
		Ratio.Grid_VisibleName = "Trans Ratio";
		Ratio.Grid_X = 1;
		Ratio.Grid_Y = 4;
		BCGridControl ratio = Ratio;
		location = new Point(122, 35);
		((Control)ratio).Location = location;
		((Control)Ratio).Name = "Ratio";
		BCGridControl ratio2 = Ratio;
		size = new Size(33, 49);
		((Control)ratio2).Size = size;
		((Control)Ratio).TabIndex = 8;
		ToolTip1.SetToolTip((Control)(object)Ratio, "Gear ratio for each gear in transmission. Modify for custom gearsets.");
		ComboBox1.DropDownStyle = (ComboBoxStyle)2;
		((ListControl)ComboBox1).FormattingEnabled = true;
		ComboBox comboBox = ComboBox1;
		location = new Point(6, 16);
		((Control)comboBox).Location = location;
		((Control)ComboBox1).Name = "ComboBox1";
		ComboBox comboBox2 = ComboBox1;
		size = new Size(110, 21);
		((Control)comboBox2).Size = size;
		((Control)ComboBox1).TabIndex = 7;
		ToolTip1.SetToolTip((Control)(object)ComboBox1, "Default transmission selections");
		((Control)GroupBox3).Controls.Add((Control)(object)OverRide_Enable);
		((Control)GroupBox3).Controls.Add((Control)(object)Label8);
		((Control)GroupBox3).Controls.Add((Control)(object)Label7);
		((Control)GroupBox3).Controls.Add((Control)(object)Label6);
		((Control)GroupBox3).Controls.Add((Control)(object)Label4);
		((Control)GroupBox3).Controls.Add((Control)(object)UpF);
		((Control)GroupBox3).Controls.Add((Control)(object)Label5);
		((Control)GroupBox3).Controls.Add((Control)(object)DownF);
		((Control)GroupBox3).Controls.Add((Control)(object)Label3);
		((Control)GroupBox3).Controls.Add((Control)(object)Offset);
		((Control)GroupBox3).Controls.Add((Control)(object)Label2);
		((Control)GroupBox3).Controls.Add((Control)(object)Slope);
		((Control)GroupBox3).Controls.Add((Control)(object)Factor);
		((Control)GroupBox3).Controls.Add((Control)(object)ComboBox2);
		((Control)GroupBox3).Controls.Add((Control)(object)OverRide_Button);
		((Control)GroupBox3).Controls.Add((Control)(object)OverRideReset_Button);
		GroupBox groupBox5 = GroupBox3;
		location = new Point(11, 153);
		((Control)groupBox5).Location = location;
		((Control)GroupBox3).Name = "GroupBox3";
		GroupBox groupBox6 = GroupBox3;
		size = new Size(595, 94);
		((Control)groupBox6).Size = size;
		((Control)GroupBox3).TabIndex = 10;
		GroupBox3.TabStop = false;
		GroupBox3.Text = "Shift Slope";
		((ButtonBase)OverRide_Enable).AutoSize = true;
		CheckBox overRide_Enable = OverRide_Enable;
		location = new Point(522, 21);
		((Control)overRide_Enable).Location = location;
		((Control)OverRide_Enable).Name = "OverRide_Enable";
		CheckBox overRide_Enable2 = OverRide_Enable;
		size = new Size(61, 17);
		((Control)overRide_Enable2).Size = size;
		((Control)OverRide_Enable).TabIndex = 20;
		((ButtonBase)OverRide_Enable).Text = "Manual";
		ToolTip1.SetToolTip((Control)(object)OverRide_Enable, "Overrides shift slope. Allows for manual specification of every point in every gear.");
		((ButtonBase)OverRide_Enable).UseVisualStyleBackColor = true;
		Label8.AutoSize = true;
		Label label7 = Label8;
		location = new Point(3, 70);
		((Control)label7).Location = location;
		((Control)Label8).Name = "Label8";
		Label label8 = Label8;
		size = new Size(35, 13);
		((Control)label8).Size = size;
		((Control)Label8).TabIndex = 19;
		Label8.Text = "Down";
		Label7.AutoSize = true;
		Label label9 = Label7;
		location = new Point(3, 58);
		((Control)label9).Location = location;
		((Control)Label7).Name = "Label7";
		Label label10 = Label7;
		size = new Size(21, 13);
		((Control)label10).Size = size;
		((Control)Label7).TabIndex = 18;
		Label7.Text = "Up";
		Label6.AutoSize = true;
		Label label11 = Label6;
		location = new Point(3, 46);
		((Control)label11).Location = location;
		((Control)Label6).Name = "Label6";
		Label label12 = Label6;
		size = new Size(31, 13);
		((Control)label12).Size = size;
		((Control)Label6).TabIndex = 17;
		Label6.Text = "Base";
		((Control)Label4).AccessibleRole = (AccessibleRole)35;
		Label4.AutoSize = true;
		Label label13 = Label4;
		location = new Point(376, 22);
		((Control)label13).Location = location;
		((Control)Label4).Name = "Label4";
		Label label14 = Label4;
		size = new Size(21, 13);
		((Control)label14).Size = size;
		((Control)Label4).TabIndex = 14;
		Label4.Text = "Up";
		ToolTip1.SetToolTip((Control)(object)Label4, "Aggressivness, on a scale of 1 to 10 of the shift curve to hold out a gear.");
		UpF.DecimalPlaces = 1;
		maximum = (UpF.Increment = new decimal(new int[4] { 1, 0, 0, 65536 }));
		NumericUpDown upF = UpF;
		location = new Point(397, 20);
		((Control)upF).Location = location;
		maximum = (UpF.Maximum = new decimal(new int[4] { 15, 0, 0, 0 }));
		maximum = (UpF.Minimum = new decimal(new int[4] { 1, 0, 0, 0 }));
		((Control)UpF).Name = "UpF";
		NumericUpDown upF2 = UpF;
		size = new Size(37, 20);
		((Control)upF2).Size = size;
		((Control)UpF).TabIndex = 13;
		maximum = (UpF.Value = new decimal(new int[4] { 5, 0, 0, 0 }));
		((Control)Label5).AccessibleRole = (AccessibleRole)35;
		Label5.AutoSize = true;
		Label label15 = Label5;
		location = new Point(440, 22);
		((Control)label15).Location = location;
		((Control)Label5).Name = "Label5";
		Label label16 = Label5;
		size = new Size(35, 13);
		((Control)label16).Size = size;
		((Control)Label5).TabIndex = 16;
		Label5.Text = "Down";
		ToolTip1.SetToolTip((Control)(object)Label5, "Aggressivness, on a scale of 1 to 10 of the shift curve to want to downshift.");
		DownF.DecimalPlaces = 1;
		maximum = (DownF.Increment = new decimal(new int[4] { 1, 0, 0, 65536 }));
		NumericUpDown downF = DownF;
		location = new Point(480, 19);
		((Control)downF).Location = location;
		maximum = (DownF.Maximum = new decimal(new int[4] { 15, 0, 0, 0 }));
		maximum = (DownF.Minimum = new decimal(new int[4] { 1, 0, 0, 0 }));
		((Control)DownF).Name = "DownF";
		NumericUpDown downF2 = DownF;
		size = new Size(36, 20);
		((Control)downF2).Size = size;
		((Control)DownF).TabIndex = 15;
		maximum = (DownF.Value = new decimal(new int[4] { 5, 0, 0, 0 }));
		((Control)Label3).AccessibleRole = (AccessibleRole)35;
		Label3.AutoSize = true;
		Label label17 = Label3;
		location = new Point(294, 22);
		((Control)label17).Location = location;
		((Control)Label3).Name = "Label3";
		Label label18 = Label3;
		size = new Size(35, 13);
		((Control)label18).Size = size;
		((Control)Label3).TabIndex = 12;
		Label3.Text = "Offset";
		ToolTip1.SetToolTip((Control)(object)Label3, "Offset the curve up or down vs TPS. Used to correct shift feel if transmission is shifting to late or early as a whole at part throttle.");
		NumericUpDown offset = Offset;
		location = new Point(330, 20);
		((Control)offset).Location = location;
		maximum = (Offset.Maximum = new decimal(new int[4] { 50, 0, 0, 0 }));
		maximum = (Offset.Minimum = new decimal(new int[4] { 50, 0, 0, -2147483648 }));
		((Control)Offset).Name = "Offset";
		NumericUpDown offset2 = Offset;
		size = new Size(40, 20);
		((Control)offset2).Size = size;
		((Control)Offset).TabIndex = 11;
		Label2.AutoSize = true;
		Label label19 = Label2;
		location = new Point(203, 22);
		((Control)label19).Location = location;
		((Control)Label2).Name = "Label2";
		Label label20 = Label2;
		size = new Size(37, 13);
		((Control)label20).Size = size;
		((Control)Label2).TabIndex = 10;
		Label2.Text = "Factor";
		ToolTip1.SetToolTip((Control)(object)Label2, "Sets base shape for shift curve. Graph the underlying table in 2D to observe the effect of changes.");
		Factor.DecimalPlaces = 2;
		maximum = (Factor.Increment = new decimal(new int[4] { 1, 0, 0, 131072 }));
		NumericUpDown factor = Factor;
		location = new Point(243, 20);
		((Control)factor).Location = location;
		maximum = (Factor.Maximum = new decimal(new int[4] { 25, 0, 0, 65536 }));
		maximum = (Factor.Minimum = new decimal(new int[4] { 25, 0, 0, 131072 }));
		((Control)Factor).Name = "Factor";
		NumericUpDown factor2 = Factor;
		size = new Size(45, 20);
		((Control)factor2).Size = size;
		((Control)Factor).TabIndex = 9;
		maximum = (Factor.Value = new decimal(new int[4] { 135, 0, 0, 131072 }));
		ComboBox2.DropDownStyle = (ComboBoxStyle)2;
		((ListControl)ComboBox2).FormattingEnabled = true;
		ComboBox comboBox3 = ComboBox2;
		location = new Point(6, 19);
		((Control)comboBox3).Location = location;
		((Control)ComboBox2).Name = "ComboBox2";
		ComboBox comboBox4 = ComboBox2;
		size = new Size(197, 21);
		((Control)comboBox4).Size = size;
		((Control)ComboBox2).TabIndex = 8;
		ToolTip1.SetToolTip((Control)(object)ComboBox2, "Throttle type to tailor shift feel for");
		Button overRide_Button = OverRide_Button;
		location = new Point(44, 50);
		((Control)overRide_Button).Location = location;
		((Control)OverRide_Button).Name = "OverRide_Button";
		Button overRide_Button2 = OverRide_Button;
		size = new Size(347, 29);
		((Control)overRide_Button2).Size = size;
		((Control)OverRide_Button).TabIndex = 21;
		((ButtonBase)OverRide_Button).Text = "Shift Slope Manual Overide";
		((ButtonBase)OverRide_Button).UseVisualStyleBackColor = true;
		Button overRideReset_Button = OverRideReset_Button;
		location = new Point(397, 50);
		((Control)overRideReset_Button).Location = location;
		((Control)OverRideReset_Button).Name = "OverRideReset_Button";
		Button overRideReset_Button2 = OverRideReset_Button;
		size = new Size(160, 29);
		((Control)overRideReset_Button2).Size = size;
		((Control)OverRideReset_Button).TabIndex = 22;
		((ButtonBase)OverRideReset_Button).Text = "Reset Overide";
		ToolTip1.SetToolTip((Control)(object)OverRideReset_Button, "Resets override data to same as selected slope data.");
		((ButtonBase)OverRideReset_Button).UseVisualStyleBackColor = true;
		((Control)Speed).BackgroundImage = (Image)componentResourceManager.GetObject("Speed.BackgroundImage");
		((Control)Speed).BackgroundImageLayout = (ImageLayout)0;
		Speed.Cell_Auto_W = 0;
		Speed.Cell_CharMax = 5;
		Speed.Cell_CPFormat = "###,###,###,##0.############";
		Speed.Cell_FontCLR = Color.Black;
		Speed.Cell_Format = "##0.0";
		Speed.Cell_FSelCLR = Color.White;
		Speed.Cell_H = 12;
		Speed.Cell_HighCLR = Color.White;
		Speed.Cell_HSelCLR = Color.DarkRed;
		Speed.Cell_LabelFormat = "####0";
		Speed.Cell_LowCLR = Color.White;
		Speed.Cell_LSelCLR = Color.Red;
		Speed.Cell_ShowChanges = 0;
		Speed.Cell_W = 32;
		Speed.Grid_AxisStatus = 0;
		Speed.Grid_DataOffset = 0f;
		Speed.Grid_DataScalar = 1f;
		Speed.Grid_DataSCopyPaste = 1;
		Speed.Grid_DataStatus = 1711;
		Speed.Grid_FreezeDraw = 0;
		Speed.Grid_GraphType = 0;
		Speed.Grid_ReDraw = 0;
		Speed.Grid_ShowLabels = 0;
		Speed.Grid_Transpose = 0;
		Speed.Grid_TransposeCopyPaste = 0;
		Speed.Grid_VisibleName = "Max Speed";
		Speed.Grid_X = 4;
		Speed.Grid_Y = 4;
		BCGridControl speed = Speed;
		location = new Point(6, 35);
		((Control)speed).Location = location;
		((Control)Speed).Name = "Speed";
		BCGridControl speed2 = Speed;
		size = new Size(129, 49);
		((Control)speed2).Size = size;
		((Control)Speed).TabIndex = 10;
		ToolTip1.SetToolTip((Control)(object)Speed, "Displays various speeds by gear. Not user changeable. For reference only.");
		((Control)GroupBox4).Controls.Add((Control)(object)Label13);
		((Control)GroupBox4).Controls.Add((Control)(object)Label12);
		((Control)GroupBox4).Controls.Add((Control)(object)Label11);
		((Control)GroupBox4).Controls.Add((Control)(object)Label10);
		((Control)GroupBox4).Controls.Add((Control)(object)Speed);
		GroupBox groupBox7 = GroupBox4;
		location = new Point(177, 27);
		((Control)groupBox7).Location = location;
		((Control)GroupBox4).Name = "GroupBox4";
		GroupBox groupBox8 = GroupBox4;
		size = new Size(142, 120);
		((Control)groupBox8).Size = size;
		((Control)GroupBox4).TabIndex = 11;
		GroupBox4.TabStop = false;
		GroupBox4.Text = "Max Speeds";
		Label13.AutoSize = true;
		Label label21 = Label13;
		location = new Point(100, 19);
		((Control)label21).Location = location;
		((Control)Label13).Name = "Label13";
		Label label22 = Label13;
		size = new Size(35, 13);
		((Control)label22).Size = size;
		((Control)Label13).TabIndex = 14;
		Label13.Text = "Down";
		Label12.AutoSize = true;
		Label label23 = Label12;
		location = new Point(74, 19);
		((Control)label23).Location = location;
		((Control)Label12).Name = "Label12";
		Label label24 = Label12;
		size = new Size(21, 13);
		((Control)label24).Size = size;
		((Control)Label12).TabIndex = 13;
		Label12.Text = "Up";
		Label11.AutoSize = true;
		Label label25 = Label11;
		location = new Point(39, 19);
		((Control)label25).Location = location;
		((Control)Label11).Name = "Label11";
		Label label26 = Label11;
		size = new Size(33, 13);
		((Control)label26).Size = size;
		((Control)Label11).TabIndex = 12;
		Label11.Text = "UnLk";
		Label10.AutoSize = true;
		Label label27 = Label10;
		location = new Point(4, 19);
		((Control)label27).Location = location;
		((Control)Label10).Name = "Label10";
		Label label28 = Label10;
		size = new Size(33, 13);
		((Control)label28).Size = size;
		((Control)Label10).TabIndex = 11;
		Label10.Text = "Lck'd";
		((Control)GroupBox5).Controls.Add((Control)(object)TireCalc);
		((Control)GroupBox5).Controls.Add((Control)(object)TireVisible);
		((Control)GroupBox5).Controls.Add((Control)(object)Label21);
		((Control)GroupBox5).Controls.Add((Control)(object)DRPM);
		((Control)GroupBox5).Controls.Add((Control)(object)Label20);
		((Control)GroupBox5).Controls.Add((Control)(object)Idle);
		((Control)GroupBox5).Controls.Add((Control)(object)Label16);
		((Control)GroupBox5).Controls.Add((Control)(object)Tire);
		((Control)GroupBox5).Controls.Add((Control)(object)Label15);
		((Control)GroupBox5).Controls.Add((Control)(object)Gear);
		((Control)GroupBox5).Controls.Add((Control)(object)Label14);
		((Control)GroupBox5).Controls.Add((Control)(object)RPM);
		GroupBox groupBox9 = GroupBox5;
		location = new Point(324, 27);
		((Control)groupBox9).Location = location;
		((Control)GroupBox5).Name = "GroupBox5";
		GroupBox groupBox10 = GroupBox5;
		size = new Size(145, 120);
		((Control)groupBox10).Size = size;
		((Control)GroupBox5).TabIndex = 12;
		GroupBox5.TabStop = false;
		GroupBox5.Text = "Engine / Drivetrain";
		Button tireCalc = TireCalc;
		location = new Point(77, 38);
		((Control)tireCalc).Location = location;
		((Control)TireCalc).Name = "TireCalc";
		Button tireCalc2 = TireCalc;
		size = new Size(14, 19);
		((Control)tireCalc2).Size = size;
		((Control)TireCalc).TabIndex = 23;
		((ButtonBase)TireCalc).Text = "C";
		((ButtonBase)TireCalc).UseVisualStyleBackColor = true;
		TireVisible.DecimalPlaces = 2;
		maximum = (TireVisible.Increment = new decimal(new int[4] { 1, 0, 0, 65536 }));
		NumericUpDown tireVisible = TireVisible;
		location = new Point(91, 38);
		((Control)tireVisible).Location = location;
		maximum = (TireVisible.Maximum = new decimal(new int[4] { 150, 0, 0, 0 }));
		maximum = (TireVisible.Minimum = new decimal(new int[4] { 5, 0, 0, 0 }));
		((Control)TireVisible).Name = "TireVisible";
		NumericUpDown tireVisible2 = TireVisible;
		size = new Size(48, 20);
		((Control)tireVisible2).Size = size;
		((Control)TireVisible).TabIndex = 22;
		maximum = (TireVisible.Value = new decimal(new int[4] { 2491, 0, 0, 131072 }));
		Label21.AutoSize = true;
		Label label29 = Label21;
		location = new Point(43, 94);
		((Control)label29).Location = location;
		((Control)Label21).Name = "Label21";
		Label label30 = Label21;
		size = new Size(42, 13);
		((Control)label30).Size = size;
		((Control)Label21).TabIndex = 21;
		Label21.Text = "D RPM";
		ToolTip1.SetToolTip((Control)(object)Label21, componentResourceManager.GetString("Label21.ToolTip"));
		maximum = (DRPM.Increment = new decimal(new int[4] { 100, 0, 0, 0 }));
		NumericUpDown dRPM = DRPM;
		location = new Point(91, 92);
		((Control)dRPM).Location = location;
		maximum = (DRPM.Maximum = new decimal(new int[4] { 9900, 0, 0, 0 }));
		maximum = (DRPM.Minimum = new decimal(new int[4] { 2000, 0, 0, 0 }));
		((Control)DRPM).Name = "DRPM";
		NumericUpDown dRPM2 = DRPM;
		size = new Size(48, 20);
		((Control)dRPM2).Size = size;
		((Control)DRPM).TabIndex = 20;
		maximum = (DRPM.Value = new decimal(new int[4] { 9900, 0, 0, 0 }));
		Label20.AutoSize = true;
		Label label31 = Label20;
		location = new Point(46, 68);
		((Control)label31).Location = location;
		((Control)Label20).Name = "Label20";
		Label label32 = Label20;
		size = new Size(24, 13);
		((Control)label32).Size = size;
		((Control)Label20).TabIndex = 19;
		Label20.Text = "Idle";
		ToolTip1.SetToolTip((Control)(object)Label20, "Idle rpm of engine when in gear.");
		maximum = (Idle.Increment = new decimal(new int[4] { 25, 0, 0, 0 }));
		NumericUpDown idle = Idle;
		location = new Point(91, 66);
		((Control)idle).Location = location;
		maximum = (Idle.Maximum = new decimal(new int[4] { 3000, 0, 0, 0 }));
		maximum = (Idle.Minimum = new decimal(new int[4] { 400, 0, 0, 0 }));
		((Control)Idle).Name = "Idle";
		NumericUpDown idle2 = Idle;
		size = new Size(48, 20);
		((Control)idle2).Size = size;
		((Control)Idle).TabIndex = 18;
		maximum = (Idle.Value = new decimal(new int[4] { 550, 0, 0, 0 }));
		Label16.AutoSize = true;
		Label label33 = Label16;
		location = new Point(46, 40);
		((Control)label33).Location = location;
		((Control)Label16).Name = "Label16";
		Label label34 = Label16;
		size = new Size(25, 13);
		((Control)label34).Size = size;
		((Control)Label16).TabIndex = 17;
		Label16.Text = "Tire";
		ToolTip1.SetToolTip((Control)(object)Label16, "Height of rear tire in inches / millimeters");
		Tire.DecimalPlaces = 2;
		maximum = (Tire.Increment = new decimal(new int[4] { 5, 0, 0, 131072 }));
		NumericUpDown tire = Tire;
		location = new Point(91, 38);
		((Control)tire).Location = location;
		maximum = (Tire.Maximum = new decimal(new int[4] { 150, 0, 0, 0 }));
		maximum = (Tire.Minimum = new decimal(new int[4] { 5, 0, 0, 0 }));
		((Control)Tire).Name = "Tire";
		NumericUpDown tire2 = Tire;
		size = new Size(48, 20);
		((Control)tire2).Size = size;
		((Control)Tire).TabIndex = 16;
		maximum = (Tire.Value = new decimal(new int[4] { 2491, 0, 0, 131072 }));
		((Control)Tire).Visible = false;
		Label15.AutoSize = true;
		Label label35 = Label15;
		location = new Point(46, 21);
		((Control)label35).Location = location;
		((Control)Label15).Name = "Label15";
		Label label36 = Label15;
		size = new Size(29, 13);
		((Control)label36).Size = size;
		((Control)Label15).TabIndex = 15;
		Label15.Text = "Final";
		ToolTip1.SetToolTip((Control)(object)Label15, "Final drive gear ratio.");
		Gear.DecimalPlaces = 2;
		maximum = (Gear.Increment = new decimal(new int[4] { 1, 0, 0, 131072 }));
		NumericUpDown gear = Gear;
		location = new Point(91, 19);
		((Control)gear).Location = location;
		maximum = (Gear.Maximum = new decimal(new int[4] { 50, 0, 0, 0 }));
		maximum = (Gear.Minimum = new decimal(new int[4] { 1, 0, 0, 0 }));
		((Control)Gear).Name = "Gear";
		NumericUpDown gear2 = Gear;
		size = new Size(48, 20);
		((Control)gear2).Size = size;
		((Control)Gear).TabIndex = 14;
		maximum = (Gear.Value = new decimal(new int[4] { 323, 0, 0, 131072 }));
		Label14.AutoSize = true;
		Label label37 = Label14;
		location = new Point(8, 19);
		((Control)label37).Location = location;
		((Control)Label14).Name = "Label14";
		Label label38 = Label14;
		size = new Size(31, 13);
		((Control)label38).Size = size;
		((Control)Label14).TabIndex = 13;
		Label14.Text = "RPM";
		((Control)RPM).BackgroundImage = (Image)componentResourceManager.GetObject("RPM.BackgroundImage");
		((Control)RPM).BackgroundImageLayout = (ImageLayout)0;
		RPM.Cell_Auto_W = 0;
		RPM.Cell_CharMax = 5;
		RPM.Cell_CPFormat = "###,###,###,##0.############";
		RPM.Cell_FontCLR = Color.Black;
		RPM.Cell_Format = "####0";
		RPM.Cell_FSelCLR = Color.White;
		RPM.Cell_H = 12;
		RPM.Cell_HighCLR = Color.White;
		RPM.Cell_HSelCLR = Color.DarkRed;
		RPM.Cell_LabelFormat = "####0";
		RPM.Cell_LowCLR = Color.White;
		RPM.Cell_LSelCLR = Color.Red;
		RPM.Cell_ShowChanges = 0;
		RPM.Cell_W = 32;
		RPM.Grid_AxisStatus = 0;
		RPM.Grid_DataOffset = 0f;
		RPM.Grid_DataScalar = 1f;
		RPM.Grid_DataSCopyPaste = 1;
		RPM.Grid_DataStatus = 542;
		RPM.Grid_FreezeDraw = 0;
		RPM.Grid_GraphType = 0;
		RPM.Grid_ReDraw = 0;
		RPM.Grid_ShowLabels = 0;
		RPM.Grid_Transpose = 0;
		RPM.Grid_TransposeCopyPaste = 0;
		RPM.Grid_VisibleName = "Engine RPM";
		RPM.Grid_X = 1;
		RPM.Grid_Y = 4;
		BCGridControl rPM = RPM;
		location = new Point(7, 35);
		((Control)rPM).Location = location;
		((Control)RPM).Name = "RPM";
		BCGridControl rPM2 = RPM;
		size = new Size(33, 49);
		((Control)rPM2).Size = size;
		((Control)RPM).TabIndex = 0;
		ToolTip1.SetToolTip((Control)(object)RPM, "Desired Shift RPMs");
		((Control)GroupBox6).Controls.Add((Control)(object)TCC_Button);
		((Control)GroupBox6).Controls.Add((Control)(object)Label25);
		((Control)GroupBox6).Controls.Add((Control)(object)WotLck);
		((Control)GroupBox6).Controls.Add((Control)(object)Label24);
		((Control)GroupBox6).Controls.Add((Control)(object)AclLck);
		((Control)GroupBox6).Controls.Add((Control)(object)Label23);
		((Control)GroupBox6).Controls.Add((Control)(object)MinLck);
		((Control)GroupBox6).Controls.Add((Control)(object)Label18);
		((Control)GroupBox6).Controls.Add((Control)(object)Stall);
		GroupBox groupBox11 = GroupBox6;
		location = new Point(478, 25);
		((Control)groupBox11).Location = location;
		((Control)GroupBox6).Name = "GroupBox6";
		GroupBox groupBox12 = GroupBox6;
		size = new Size(128, 122);
		((Control)groupBox12).Size = size;
		((Control)GroupBox6).TabIndex = 13;
		GroupBox6.TabStop = false;
		GroupBox6.Text = "Torque Converter";
		Button tCC_Button = TCC_Button;
		location = new Point(6, 92);
		((Control)tCC_Button).Location = location;
		((Control)TCC_Button).Name = "TCC_Button";
		Button tCC_Button2 = TCC_Button;
		size = new Size(110, 24);
		((Control)tCC_Button2).Size = size;
		((Control)TCC_Button).TabIndex = 30;
		((ButtonBase)TCC_Button).Text = "Lockup Config";
		ToolTip1.SetToolTip((Control)(object)TCC_Button, "Lockup configuration form.");
		((ButtonBase)TCC_Button).UseVisualStyleBackColor = true;
		Label25.AutoSize = true;
		Label label39 = Label25;
		location = new Point(8, 73);
		((Control)label39).Location = location;
		((Control)Label25).Name = "Label25";
		Label label40 = Label25;
		size = new Size(59, 13);
		((Control)label40).Size = size;
		((Control)Label25).TabIndex = 29;
		Label25.Text = "WOT Gear";
		ToolTip1.SetToolTip((Control)(object)Label25, "Lowest gear that the converter is allowed to lockup in during WOT. Setting to a value higher\r\n that the highest gear disables lockup at WOT.");
		NumericUpDown wotLck = WotLck;
		location = new Point(84, 71);
		((Control)wotLck).Location = location;
		maximum = (WotLck.Maximum = new decimal(new int[4] { 10, 0, 0, 0 }));
		maximum = (WotLck.Minimum = new decimal(new int[4] { 1, 0, 0, 0 }));
		((Control)WotLck).Name = "WotLck";
		NumericUpDown wotLck2 = WotLck;
		size = new Size(32, 20);
		((Control)wotLck2).Size = size;
		((Control)WotLck).TabIndex = 28;
		maximum = (WotLck.Value = new decimal(new int[4] { 5, 0, 0, 0 }));
		Label24.AutoSize = true;
		Label label41 = Label24;
		location = new Point(7, 55);
		((Control)label41).Location = location;
		((Control)Label24).Name = "Label24";
		Label label42 = Label24;
		size = new Size(60, 13);
		((Control)label42).Size = size;
		((Control)Label24).TabIndex = 27;
		Label24.Text = "Accel Gear";
		ToolTip1.SetToolTip((Control)(object)Label24, componentResourceManager.GetString("Label24.ToolTip"));
		NumericUpDown aclLck = AclLck;
		location = new Point(84, 53);
		((Control)aclLck).Location = location;
		maximum = (AclLck.Maximum = new decimal(new int[4] { 10, 0, 0, 0 }));
		maximum = (AclLck.Minimum = new decimal(new int[4] { 1, 0, 0, 0 }));
		((Control)AclLck).Name = "AclLck";
		NumericUpDown aclLck2 = AclLck;
		size = new Size(32, 20);
		((Control)aclLck2).Size = size;
		((Control)AclLck).TabIndex = 26;
		maximum = (AclLck.Value = new decimal(new int[4] { 4, 0, 0, 0 }));
		Label23.AutoSize = true;
		Label label43 = Label23;
		location = new Point(7, 37);
		((Control)label43).Location = location;
		((Control)Label23).Name = "Label23";
		Label label44 = Label23;
		size = new Size(50, 13);
		((Control)label44).Size = size;
		((Control)Label23).TabIndex = 25;
		Label23.Text = "Min Gear";
		ToolTip1.SetToolTip((Control)(object)Label23, "Lowest gear that converter lockup is allowed under any circumstance. Setting to a value\r\n higher than the highest gear disables normal lockup completely.");
		NumericUpDown minLck = MinLck;
		location = new Point(84, 35);
		((Control)minLck).Location = location;
		maximum = (MinLck.Maximum = new decimal(new int[4] { 10, 0, 0, 0 }));
		maximum = (MinLck.Minimum = new decimal(new int[4] { 1, 0, 0, 0 }));
		((Control)MinLck).Name = "MinLck";
		NumericUpDown minLck2 = MinLck;
		size = new Size(32, 20);
		((Control)minLck2).Size = size;
		((Control)MinLck).TabIndex = 24;
		maximum = (MinLck.Value = new decimal(new int[4] { 3, 0, 0, 0 }));
		Label18.AutoSize = true;
		Label label45 = Label18;
		location = new Point(7, 19);
		((Control)label45).Location = location;
		((Control)Label18).Name = "Label18";
		Label label46 = Label18;
		size = new Size(27, 13);
		((Control)label46).Size = size;
		((Control)Label18).TabIndex = 13;
		Label18.Text = "Stall";
		ToolTip1.SetToolTip((Control)(object)Label18, componentResourceManager.GetString("Label18.ToolTip"));
		maximum = (Stall.Increment = new decimal(new int[4] { 50, 0, 0, 0 }));
		NumericUpDown stall = Stall;
		location = new Point(63, 16);
		((Control)stall).Location = location;
		maximum = (Stall.Maximum = new decimal(new int[4] { 8000, 0, 0, 0 }));
		maximum = (Stall.Minimum = new decimal(new int[4] { 1000, 0, 0, 0 }));
		((Control)Stall).Name = "Stall";
		NumericUpDown stall2 = Stall;
		size = new Size(53, 20);
		((Control)stall2).Size = size;
		((Control)Stall).TabIndex = 12;
		maximum = (Stall.Value = new decimal(new int[4] { 2000, 0, 0, 0 }));
		Timer1.Enabled = true;
		Timer1.Interval = 50;
		((ToolStrip)MenuStrip1).Items.AddRange((ToolStripItem[])(object)new ToolStripItem[4]
		{
			(ToolStripItem)FileToolStripMenuItem,
			(ToolStripItem)ExportToolStripMenuItem,
			(ToolStripItem)OptionsToolStripMenuItem,
			(ToolStripItem)HelpToolStripMenuItem
		});
		MenuStrip menuStrip = MenuStrip1;
		location = new Point(0, 0);
		((Control)menuStrip).Location = location;
		((Control)MenuStrip1).Name = "MenuStrip1";
		MenuStrip menuStrip2 = MenuStrip1;
		size = new Size(620, 24);
		((Control)menuStrip2).Size = size;
		((Control)MenuStrip1).TabIndex = 14;
		((Control)MenuStrip1).Text = "MenuStrip1";
		((ToolStripDropDownItem)FileToolStripMenuItem).DropDownItems.AddRange((ToolStripItem[])(object)new ToolStripItem[2]
		{
			(ToolStripItem)OpenToolStripMenuItem,
			(ToolStripItem)SaveToolStripMenuItem
		});
		((ToolStripItem)FileToolStripMenuItem).Name = "FileToolStripMenuItem";
		ToolStripMenuItem fileToolStripMenuItem = FileToolStripMenuItem;
		size = new Size(37, 20);
		((ToolStripItem)fileToolStripMenuItem).Size = size;
		((ToolStripItem)FileToolStripMenuItem).Text = "File";
		((ToolStripItem)OpenToolStripMenuItem).Name = "OpenToolStripMenuItem";
		ToolStripMenuItem openToolStripMenuItem = OpenToolStripMenuItem;
		size = new Size(103, 22);
		((ToolStripItem)openToolStripMenuItem).Size = size;
		((ToolStripItem)OpenToolStripMenuItem).Text = "Open";
		((ToolStripItem)SaveToolStripMenuItem).Name = "SaveToolStripMenuItem";
		ToolStripMenuItem saveToolStripMenuItem = SaveToolStripMenuItem;
		size = new Size(103, 22);
		((ToolStripItem)saveToolStripMenuItem).Size = size;
		((ToolStripItem)SaveToolStripMenuItem).Text = "Save";
		((ToolStripDropDownItem)ExportToolStripMenuItem).DropDownItems.AddRange((ToolStripItem[])(object)new ToolStripItem[1] { (ToolStripItem)ExportWindowToolStripMenuItem });
		((ToolStripItem)ExportToolStripMenuItem).Name = "ExportToolStripMenuItem";
		ToolStripMenuItem exportToolStripMenuItem = ExportToolStripMenuItem;
		size = new Size(52, 20);
		((ToolStripItem)exportToolStripMenuItem).Size = size;
		((ToolStripItem)ExportToolStripMenuItem).Text = "Export";
		((ToolStripItem)ExportWindowToolStripMenuItem).Name = "ExportWindowToolStripMenuItem";
		ToolStripMenuItem exportWindowToolStripMenuItem = ExportWindowToolStripMenuItem;
		size = new Size(154, 22);
		((ToolStripItem)exportWindowToolStripMenuItem).Size = size;
		((ToolStripItem)ExportWindowToolStripMenuItem).Text = "Export Window";
		((ToolStripItem)ExportWindowToolStripMenuItem).ToolTipText = "Table layouts specifically for pasting into tuning software.";
		((ToolStripDropDownItem)OptionsToolStripMenuItem).DropDownItems.AddRange((ToolStripItem[])(object)new ToolStripItem[13]
		{
			(ToolStripItem)Metric,
			(ToolStripItem)DynoMode,
			(ToolStripItem)RRM,
			(ToolStripItem)SGS,
			(ToolStripItem)StallLogic,
			(ToolStripItem)MaxSpeed_Locked,
			(ToolStripItem)ULckStay,
			(ToolStripItem)LeadRpm,
			(ToolStripItem)Allow4L60WOT4th,
			(ToolStripItem)WOTTCCPrep,
			(ToolStripItem)No2CT_6L,
			(ToolStripItem)LogicChecksRulesToolStripMenuItem,
			(ToolStripItem)ShiftAndLockMinSpreadsToolStripMenuItem
		});
		((ToolStripItem)OptionsToolStripMenuItem).Name = "OptionsToolStripMenuItem";
		ToolStripMenuItem optionsToolStripMenuItem = OptionsToolStripMenuItem;
		size = new Size(61, 20);
		((ToolStripItem)optionsToolStripMenuItem).Size = size;
		((ToolStripItem)OptionsToolStripMenuItem).Text = "Options";
		Metric.CheckOnClick = true;
		((ToolStripItem)Metric).Name = "Metric";
		ToolStripMenuItem metric = Metric;
		size = new Size(296, 22);
		((ToolStripItem)metric).Size = size;
		((ToolStripItem)Metric).Text = "Metric Units";
		((ToolStripItem)Metric).ToolTipText = "Imperial or Metric units of measure.";
		DynoMode.CheckOnClick = true;
		((ToolStripItem)DynoMode).Name = "DynoMode";
		ToolStripMenuItem dynoMode = DynoMode;
		size = new Size(296, 22);
		((ToolStripItem)dynoMode).Size = size;
		((ToolStripItem)DynoMode).Text = "Dyno Mode";
		((ToolStripItem)DynoMode).ToolTipText = "Sets up the trans tables for dyno use. Prevents downshifting and keeps converter \r\nlocked for gears that it is enabled.";
		RRM.CheckOnClick = true;
		((ToolStripItem)RRM).Name = "RRM";
		ToolStripMenuItem rRM = RRM;
		size = new Size(296, 22);
		((ToolStripItem)rRM).Size = size;
		((ToolStripItem)RRM).Text = "Roll Race Mode";
		((ToolStripItem)RRM).ToolTipText = "Sets up the trans tables for roll racing, Applys WOT shifts at part throttle.";
		SGS.CheckOnClick = true;
		((ToolStripItem)SGS).Name = "SGS";
		ToolStripMenuItem sGS = SGS;
		size = new Size(296, 22);
		((ToolStripItem)sGS).Size = size;
		((ToolStripItem)SGS).Text = "2nd Gear Start";
		((ToolStripItem)SGS).ToolTipText = "Sets up the trans tables for starting off in 2nd gear";
		StallLogic.Checked = true;
		StallLogic.CheckOnClick = true;
		StallLogic.CheckState = (CheckState)1;
		((ToolStripItem)StallLogic).Name = "StallLogic";
		ToolStripMenuItem stallLogic = StallLogic;
		size = new Size(296, 22);
		((ToolStripItem)stallLogic).Size = size;
		((ToolStripItem)StallLogic).Text = "Use Lockup Cushion Stall Logic";
		((ToolStripItem)StallLogic).ToolTipText = componentResourceManager.GetString("StallLogic.ToolTipText");
		MaxSpeed_Locked.Checked = true;
		MaxSpeed_Locked.CheckOnClick = true;
		MaxSpeed_Locked.CheckState = (CheckState)1;
		((ToolStripItem)MaxSpeed_Locked).Name = "MaxSpeed_Locked";
		ToolStripMenuItem maxSpeed_Locked = MaxSpeed_Locked;
		size = new Size(296, 22);
		((ToolStripItem)maxSpeed_Locked).Size = size;
		((ToolStripItem)MaxSpeed_Locked).Text = "Shift Speed Assessed by Converter Lockup";
		((ToolStripItem)MaxSpeed_Locked).ToolTipText = "Adjusts WOT shift speeds based of if the converter is lock or not when the shift occurs.";
		ULckStay.Checked = true;
		ULckStay.CheckOnClick = true;
		ULckStay.CheckState = (CheckState)1;
		((ToolStripItem)ULckStay).Name = "ULckStay";
		ToolStripMenuItem uLckStay = ULckStay;
		size = new Size(296, 22);
		((ToolStripItem)uLckStay).Size = size;
		((ToolStripItem)ULckStay).Text = "Unlock before Downshift - Stay Unlocked";
		((ToolStripItem)ULckStay).ToolTipText = "If the converter is already unlocked during a downshift, keep it unlocked if decelerating.";
		LeadRpm.Checked = true;
		LeadRpm.CheckOnClick = true;
		LeadRpm.CheckState = (CheckState)1;
		((ToolStripItem)LeadRpm).Name = "LeadRpm";
		ToolStripMenuItem leadRpm = LeadRpm;
		size = new Size(296, 22);
		((ToolStripItem)leadRpm).Size = size;
		((ToolStripItem)LeadRpm).Text = "Export Shift RPM Based off Lead";
		((ToolStripItem)LeadRpm).ToolTipText = "As a function of the shift lead time, this scales the shift rpm's back proportionate to what the lead \r\ndid with the shift mph. Only makes changes to the output values in the export window.";
		Allow4L60WOT4th.Checked = true;
		Allow4L60WOT4th.CheckOnClick = true;
		Allow4L60WOT4th.CheckState = (CheckState)1;
		((ToolStripItem)Allow4L60WOT4th).Name = "Allow4L60WOT4th";
		ToolStripMenuItem allow4L60WOT4th = Allow4L60WOT4th;
		size = new Size(296, 22);
		((ToolStripItem)allow4L60WOT4th).Size = size;
		((ToolStripItem)Allow4L60WOT4th).Text = "Allow 4L60e WOT 4th Shift";
		((ToolStripItem)Allow4L60WOT4th).ToolTipText = "Junk 4L60 transmissions can damage themselves if allowed to upshift to overdrive at WOT. Most\r\n stock tunes do not allow this.";
		WOTTCCPrep.Checked = true;
		WOTTCCPrep.CheckOnClick = true;
		WOTTCCPrep.CheckState = (CheckState)1;
		((ToolStripItem)WOTTCCPrep).Name = "WOTTCCPrep";
		ToolStripMenuItem wOTTCCPrep = WOTTCCPrep;
		size = new Size(296, 22);
		((ToolStripItem)wOTTCCPrep).Size = size;
		((ToolStripItem)WOTTCCPrep).Text = "6Lxx/8Lxx/10Lxx WOT TCC Prep";
		((ToolStripItem)WOTTCCPrep).ToolTipText = "False enable early to defeat any dealy timers that inhibit activation.";
		No2CT_6L.Checked = true;
		No2CT_6L.CheckOnClick = true;
		No2CT_6L.CheckState = (CheckState)1;
		((ToolStripItem)No2CT_6L).Name = "No2CT_6L";
		ToolStripMenuItem no2CT_6L = No2CT_6L;
		size = new Size(296, 22);
		((ToolStripItem)no2CT_6L).Size = size;
		((ToolStripItem)No2CT_6L).Text = "6Lxx/8Lxx/10Lxx Skip 2nd on CT Downshift";
		((ToolStripItem)No2CT_6L).ToolTipText = "Skip 2nd gear on closed throttle downshifts. Prevents clunking on some transmissions.";
		((ToolStripDropDownItem)LogicChecksRulesToolStripMenuItem).DropDownItems.AddRange((ToolStripItem[])(object)new ToolStripItem[6]
		{
			(ToolStripItem)InitLock,
			(ToolStripItem)PreLock,
			(ToolStripItem)PostLock,
			(ToolStripItem)LockUnlock,
			(ToolStripItem)UpDown,
			(ToolStripItem)ShiftMax
		});
		((ToolStripItem)LogicChecksRulesToolStripMenuItem).Name = "LogicChecksRulesToolStripMenuItem";
		ToolStripMenuItem logicChecksRulesToolStripMenuItem = LogicChecksRulesToolStripMenuItem;
		size = new Size(296, 22);
		((ToolStripItem)logicChecksRulesToolStripMenuItem).Size = size;
		((ToolStripItem)LogicChecksRulesToolStripMenuItem).Text = "Logic Checks and Rules";
		InitLock.Checked = true;
		InitLock.CheckOnClick = true;
		InitLock.CheckState = (CheckState)1;
		((ToolStripItem)InitLock).Name = "InitLock";
		ToolStripMenuItem initLock = InitLock;
		size = new Size(276, 22);
		((ToolStripItem)initLock).Size = size;
		((ToolStripItem)InitLock).Text = "Initial Lock During Accel Gear";
		((ToolStripItem)InitLock).ToolTipText = "Ensures normal lockup event to occure during the lockup accel gear.";
		PreLock.Checked = true;
		PreLock.CheckOnClick = true;
		PreLock.CheckState = (CheckState)1;
		((ToolStripItem)PreLock).Name = "PreLock";
		ToolStripMenuItem preLock = PreLock;
		size = new Size(276, 22);
		((ToolStripItem)preLock).Size = size;
		((ToolStripItem)PreLock).Text = "Upshift Before Lockup Pre Accel Gear";
		((ToolStripItem)PreLock).ToolTipText = "Ensures converter does not lock before shiftring on gears before the converter accel lock gear.";
		PostLock.Checked = true;
		PostLock.CheckOnClick = true;
		PostLock.CheckState = (CheckState)1;
		((ToolStripItem)PostLock).Name = "PostLock";
		ToolStripMenuItem postLock = PostLock;
		size = new Size(276, 22);
		((ToolStripItem)postLock).Size = size;
		((ToolStripItem)PostLock).Text = "Lockup Before Upshift Post Accel Gear";
		((ToolStripItem)PostLock).ToolTipText = "Ensures converter is set to already be locked before shiftring into gears after the converter accel lock gear.";
		LockUnlock.Checked = true;
		LockUnlock.CheckOnClick = true;
		LockUnlock.CheckState = (CheckState)1;
		((ToolStripItem)LockUnlock).Name = "LockUnlock";
		ToolStripMenuItem lockUnlock = LockUnlock;
		size = new Size(276, 22);
		((ToolStripItem)lockUnlock).Size = size;
		((ToolStripItem)LockUnlock).Text = "Lockup > Unlock";
		((ToolStripItem)LockUnlock).ToolTipText = "Ensures that the lockup speed is higher than the unlock speed for any given gear. Difference is \r\ncontrolled by the appropriate value under minumim spreads.";
		UpDown.Checked = true;
		UpDown.CheckOnClick = true;
		UpDown.CheckState = (CheckState)1;
		((ToolStripItem)UpDown).Name = "UpDown";
		ToolStripMenuItem upDown = UpDown;
		size = new Size(276, 22);
		((ToolStripItem)upDown).Size = size;
		((ToolStripItem)UpDown).Text = "Upshift > Downshift";
		((ToolStripItem)UpDown).ToolTipText = "Ensures that the upshift speed is higher than the downshift speed for any given gear. Difference is \r\ncontrolled by the appropriate value under minumim spreads.";
		ShiftMax.Checked = true;
		ShiftMax.CheckOnClick = true;
		ShiftMax.CheckState = (CheckState)1;
		((ToolStripItem)ShiftMax).Name = "ShiftMax";
		ToolStripMenuItem shiftMax = ShiftMax;
		size = new Size(276, 22);
		((ToolStripItem)shiftMax).Size = size;
		((ToolStripItem)ShiftMax).Text = "Shift < Max Speed";
		((ToolStripItem)ShiftMax).ToolTipText = "Ensures all values are less than the max speed for each gear.";
		((ToolStripDropDownItem)ShiftAndLockMinSpreadsToolStripMenuItem).DropDownItems.AddRange((ToolStripItem[])(object)new ToolStripItem[4]
		{
			(ToolStripItem)MinShiftToDownshiftSpreadToolStripMenuItem,
			(ToolStripItem)MinLockToUnlockSpreadToolStripMenuItem,
			(ToolStripItem)Shift_Lock_Spread,
			(ToolStripItem)ToolStripMenuItem1
		});
		((ToolStripItem)ShiftAndLockMinSpreadsToolStripMenuItem).Name = "ShiftAndLockMinSpreadsToolStripMenuItem";
		ToolStripMenuItem shiftAndLockMinSpreadsToolStripMenuItem = ShiftAndLockMinSpreadsToolStripMenuItem;
		size = new Size(296, 22);
		((ToolStripItem)shiftAndLockMinSpreadsToolStripMenuItem).Size = size;
		((ToolStripItem)ShiftAndLockMinSpreadsToolStripMenuItem).Text = "Shift and Lock Minimum Spreads";
		((ToolStripDropDownItem)MinShiftToDownshiftSpreadToolStripMenuItem).DropDownItems.AddRange((ToolStripItem[])(object)new ToolStripItem[1] { (ToolStripItem)Shift_Spread });
		((ToolStripItem)MinShiftToDownshiftSpreadToolStripMenuItem).Name = "MinShiftToDownshiftSpreadToolStripMenuItem";
		ToolStripMenuItem minShiftToDownshiftSpreadToolStripMenuItem = MinShiftToDownshiftSpreadToolStripMenuItem;
		size = new Size(253, 22);
		((ToolStripItem)minShiftToDownshiftSpreadToolStripMenuItem).Size = size;
		((ToolStripItem)MinShiftToDownshiftSpreadToolStripMenuItem).Text = "Min Upshift <> Downshift Spread";
		((ToolStripItem)Shift_Spread).Name = "Shift_Spread";
		ToolStripTextBox shift_Spread = Shift_Spread;
		size = new Size(100, 23);
		((ToolStripControlHost)shift_Spread).Size = size;
		((ToolStripControlHost)Shift_Spread).Text = "3";
		((ToolStripDropDownItem)MinLockToUnlockSpreadToolStripMenuItem).DropDownItems.AddRange((ToolStripItem[])(object)new ToolStripItem[1] { (ToolStripItem)Lock_Spread });
		((ToolStripItem)MinLockToUnlockSpreadToolStripMenuItem).Name = "MinLockToUnlockSpreadToolStripMenuItem";
		ToolStripMenuItem minLockToUnlockSpreadToolStripMenuItem = MinLockToUnlockSpreadToolStripMenuItem;
		size = new Size(253, 22);
		((ToolStripItem)minLockToUnlockSpreadToolStripMenuItem).Size = size;
		((ToolStripItem)MinLockToUnlockSpreadToolStripMenuItem).Text = "Min Lock <> Unlock Spread";
		((ToolStripItem)Lock_Spread).Name = "Lock_Spread";
		ToolStripTextBox lock_Spread = Lock_Spread;
		size = new Size(100, 23);
		((ToolStripControlHost)lock_Spread).Size = size;
		((ToolStripControlHost)Lock_Spread).Text = "2";
		((ToolStripDropDownItem)Shift_Lock_Spread).DropDownItems.AddRange((ToolStripItem[])(object)new ToolStripItem[1] { (ToolStripItem)Lock_Shift_Spread });
		((ToolStripItem)Shift_Lock_Spread).Name = "Shift_Lock_Spread";
		ToolStripMenuItem shift_Lock_Spread = Shift_Lock_Spread;
		size = new Size(253, 22);
		((ToolStripItem)shift_Lock_Spread).Size = size;
		((ToolStripItem)Shift_Lock_Spread).Text = "Min Lock <> Upshift Spread";
		((ToolStripItem)Lock_Shift_Spread).Name = "Lock_Shift_Spread";
		ToolStripTextBox lock_Shift_Spread = Lock_Shift_Spread;
		size = new Size(100, 23);
		((ToolStripControlHost)lock_Shift_Spread).Size = size;
		((ToolStripControlHost)Lock_Shift_Spread).Text = "4";
		((ToolStripDropDownItem)ToolStripMenuItem1).DropDownItems.AddRange((ToolStripItem[])(object)new ToolStripItem[1] { (ToolStripItem)Unlock_Shift_Spread });
		((ToolStripItem)ToolStripMenuItem1).Name = "ToolStripMenuItem1";
		ToolStripMenuItem toolStripMenuItem = ToolStripMenuItem1;
		size = new Size(253, 22);
		((ToolStripItem)toolStripMenuItem).Size = size;
		((ToolStripItem)ToolStripMenuItem1).Text = "Min UnLock <> Downshift Spread";
		((ToolStripItem)Unlock_Shift_Spread).Name = "Unlock_Shift_Spread";
		ToolStripTextBox unlock_Shift_Spread = Unlock_Shift_Spread;
		size = new Size(100, 23);
		((ToolStripControlHost)unlock_Shift_Spread).Size = size;
		((ToolStripControlHost)Unlock_Shift_Spread).Text = "1";
		((ToolStripDropDownItem)HelpToolStripMenuItem).DropDownItems.AddRange((ToolStripItem[])(object)new ToolStripItem[1] { (ToolStripItem)AboutToolStripMenuItem });
		((ToolStripItem)HelpToolStripMenuItem).Name = "HelpToolStripMenuItem";
		ToolStripMenuItem helpToolStripMenuItem = HelpToolStripMenuItem;
		size = new Size(44, 20);
		((ToolStripItem)helpToolStripMenuItem).Size = size;
		((ToolStripItem)HelpToolStripMenuItem).Text = "Help";
		((ToolStripItem)AboutToolStripMenuItem).Name = "AboutToolStripMenuItem";
		ToolStripMenuItem aboutToolStripMenuItem = AboutToolStripMenuItem;
		size = new Size(152, 22);
		((ToolStripItem)aboutToolStripMenuItem).Size = size;
		((ToolStripItem)AboutToolStripMenuItem).Text = "About";
		((FileDialog)OpenFileDialog1).FileName = "*.BTC";
		((FileDialog)OpenFileDialog1).Filter = "Bluecat Transmission Configuration Files (*.BTC)|*.BTC";
		((FileDialog)OpenFileDialog1).InitialDirectory = ".";
		((FileDialog)OpenFileDialog1).Title = "Open Transmission File";
		((FileDialog)SaveFileDialog1).DefaultExt = "BTC";
		((FileDialog)SaveFileDialog1).Filter = "Bluecat Transmission Configuration Files (*.BTC)|*.BTC";
		((FileDialog)SaveFileDialog1).InitialDirectory = ".";
		((FileDialog)SaveFileDialog1).Title = "Save Transmission File";
		ToolTip1.AutomaticDelay = 25000;
		ToolTip1.AutoPopDelay = 25000;
		ToolTip1.InitialDelay = 1000;
		ToolTip1.ReshowDelay = 1000;
		Label19.AutoSize = true;
		Label label47 = Label19;
		location = new Point(521, 5);
		((Control)label47).Location = location;
		((Control)Label19).Name = "Label19";
		Label label48 = Label19;
		size = new Size(0, 13);
		((Control)label48).Size = size;
		((Control)Label19).TabIndex = 15;
		SizeF autoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleDimensions = autoScaleDimensions;
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		size = new Size(620, 516);
		((Form)this).ClientSize = size;
		((Control)this).Controls.Add((Control)(object)Label19);
		((Control)this).Controls.Add((Control)(object)GroupBox6);
		((Control)this).Controls.Add((Control)(object)GroupBox5);
		((Control)this).Controls.Add((Control)(object)GroupBox4);
		((Control)this).Controls.Add((Control)(object)GroupBox3);
		((Control)this).Controls.Add((Control)(object)GroupBox2);
		((Control)this).Controls.Add((Control)(object)GroupBox1);
		((Control)this).Controls.Add((Control)(object)BcGridControl1);
		((Control)this).Controls.Add((Control)(object)MenuStrip1);
		((Control)this).DoubleBuffered = true;
		((Form)this).FormBorderStyle = (FormBorderStyle)1;
		((Form)this).Icon = (Icon)componentResourceManager.GetObject("$this.Icon");
		((Form)this).MainMenuStrip = MenuStrip1;
		((Form)this).MaximizeBox = false;
		((Control)this).Name = "Main_Form";
		((Form)this).StartPosition = (FormStartPosition)1;
		((Form)this).Text = "Tuned by Bluecat - Bluecat Trans Cal Generator 1.42 - tunedbybluecat@gmail.com";
		((ISupportInitialize)Gears).EndInit();
		((Control)GroupBox1).ResumeLayout(false);
		((Control)GroupBox2).ResumeLayout(false);
		((Control)GroupBox2).PerformLayout();
		((ISupportInitialize)VSS).EndInit();
		((Control)GroupBox3).ResumeLayout(false);
		((Control)GroupBox3).PerformLayout();
		((ISupportInitialize)UpF).EndInit();
		((ISupportInitialize)DownF).EndInit();
		((ISupportInitialize)Offset).EndInit();
		((ISupportInitialize)Factor).EndInit();
		((Control)GroupBox4).ResumeLayout(false);
		((Control)GroupBox4).PerformLayout();
		((Control)GroupBox5).ResumeLayout(false);
		((Control)GroupBox5).PerformLayout();
		((ISupportInitialize)TireVisible).EndInit();
		((ISupportInitialize)DRPM).EndInit();
		((ISupportInitialize)Idle).EndInit();
		((ISupportInitialize)Tire).EndInit();
		((ISupportInitialize)Gear).EndInit();
		((Control)GroupBox6).ResumeLayout(false);
		((Control)GroupBox6).PerformLayout();
		((ISupportInitialize)WotLck).EndInit();
		((ISupportInitialize)AclLck).EndInit();
		((ISupportInitialize)MinLck).EndInit();
		((ISupportInitialize)Stall).EndInit();
		((Control)MenuStrip1).ResumeLayout(false);
		((Control)MenuStrip1).PerformLayout();
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}

	private void Main_Form_Load(object sender, EventArgs e)
	{
		((Control)MyProject.Forms.Lead_Form).Show();
		((Control)MyProject.Forms.Lead_Form).Hide();
		((Control)MyProject.Forms.TCC_Form).Show();
		((Control)MyProject.Forms.TCC_Form).Hide();
		((Control)MyProject.Forms.Export_Form).Show();
		((Control)MyProject.Forms.Export_Form).Hide();
		((Control)MyProject.Forms.OverRide_Form).Show();
		((Control)MyProject.Forms.OverRide_Form).Hide();
		((Control)MyProject.Forms.Logo_Form).Show();
	}

	private void Setup_Form()
	{
		Load_Presets();
		ComboBox1.Items.Clear();
		ComboBox1.Items.Add((object)"Custom");
		foreach (Trans_Preset transPreset in TransPresets)
		{
			ComboBox1.Items.Add((object)transPreset.Name);
		}
		ComboBox1.SelectedIndex = 0;
		ComboBox2.Items.Clear();
		ComboBox2.Items.Add((object)"Custom");
		foreach (Slope_Preset slopePreset in SlopePresets)
		{
			ComboBox2.Items.Add((object)slopePreset.Name);
		}
		if (ComboBox2.Items.Count > 1)
		{
			ComboBox2.SelectedIndex = 1;
		}
		else
		{
			ComboBox2.SelectedIndex = 0;
		}
		MyProject.Forms.Lead_Form.Lead_Radio2.Checked = true;
		MyProject.Forms.Export_Form.ComboBox1.Items.Clear();
		MyProject.Forms.Export_Form.ComboBox1.Items.Add((object)"(None)");
		MyProject.Forms.Export_Form.ComboBox1.Items.Add((object)"GM 4-Speed P01/P59");
		MyProject.Forms.Export_Form.ComboBox1.Items.Add((object)"GM 4-Speed T42");
		MyProject.Forms.Export_Form.ComboBox1.Items.Add((object)"GM 6-Speed T43");
		MyProject.Forms.Export_Form.ComboBox1.Items.Add((object)"GM 6-Speed T43 Late");
		MyProject.Forms.Export_Form.ComboBox1.Items.Add((object)"GM 8-Speed T87/T87a");
		MyProject.Forms.Export_Form.ComboBox1.Items.Add((object)"GM 8-Speed T93a");
		MyProject.Forms.Export_Form.ComboBox1.Items.Add((object)"GM 10-Speed T87a/T93");
		MyProject.Forms.Export_Form.ComboBox1.SelectedIndex = 0;
		MyProject.Forms.Export_Form.ComboBox2.Items.Clear();
		MyProject.Forms.Export_Form.ComboBox2.Items.Add((object)"Gen III 98");
		MyProject.Forms.Export_Form.ComboBox2.Items.Add((object)"Gen III 97-98 Vette");
		MyProject.Forms.Export_Form.ComboBox2.Items.Add((object)"Gen III");
		MyProject.Forms.Export_Form.ComboBox2.Items.Add((object)"Gen III Vette");
		MyProject.Forms.Export_Form.ComboBox2.Items.Add((object)"Gen IV/V");
		MyProject.Forms.Export_Form.ComboBox2.Items.Add((object)"Gen IV 05 Vette");
		MyProject.Forms.Export_Form.ComboBox2.SelectedIndex = 2;
	}

	private void ComboBox1_SelectedIndexChanged(object sender, EventArgs e)
	{
		checked
		{
			if (Init >= 2)
			{
				int selectedIndex = ComboBox1.SelectedIndex;
				if ((selectedIndex >= 1) & (selectedIndex <= TransPresets.Count))
				{
					Apply_Trans_Preset(TransPresets[selectedIndex - 1]);
					ComboBox1.SelectedIndex = selectedIndex;
				}
				else
				{
					MyProject.Forms.Export_Form.Set_Export_Options(new int[1] { 0 });
				}
				US++;
			}
		}
	}

	private void ComboBox2_SelectedIndexChanged(object sender, EventArgs e)
	{
		if (Init >= 1)
		{
			int selectedIndex = ComboBox2.SelectedIndex;
			if ((selectedIndex >= 1) & (selectedIndex <= SlopePresets.Count))
			{
				Slope_Preset slope_Preset = SlopePresets[checked(selectedIndex - 1)];
				Factor.Value = ClampD(new decimal(slope_Preset.Factor), Factor.Minimum, Factor.Maximum);
				Offset.Value = ClampD(new decimal(slope_Preset.Offset), Offset.Minimum, Offset.Maximum);
				UpF.Value = ClampD(new decimal(slope_Preset.UpF), UpF.Minimum, UpF.Maximum);
				DownF.Value = ClampD(new decimal(slope_Preset.DownF), DownF.Minimum, DownF.Maximum);
				ComboBox2.SelectedIndex = selectedIndex;
			}
			Update_Slope();
		}
	}

	private void Apply_Trans_Preset(Trans_Preset tp)
	{
		Gears.Value = new decimal(tp.Gears);
		VSS.Value = ClampD(new decimal(tp.VSS), VSS.Minimum, VSS.Maximum);
		MyProject.Forms.Lead_Form.Lead.Value = ClampD(new decimal(tp.Lead), MyProject.Forms.Lead_Form.Lead.Minimum, MyProject.Forms.Lead_Form.Lead.Maximum);
		int gears = tp.Gears;
		checked
		{
			for (int i = 1; i <= gears; i++)
			{
				Ratio.W_Data(1, (byte)i, tp.Ratios[i]);
			}
			int num = tp.Gears - 1;
			for (int j = 1; j <= num; j++)
			{
				MyProject.Forms.Lead_Form.Delay.W_Data(1, (byte)j, tp.Preps[j]);
				MyProject.Forms.Lead_Form.Delay.W_Data(2, (byte)j, tp.Reacts[j]);
			}
			MyProject.Forms.Export_Form.Set_Export_Options(tp.ExportModes);
		}
	}

	private decimal ClampD(decimal v, decimal lo, decimal hi)
	{
		if (decimal.Compare(v, lo) < 0)
		{
			return lo;
		}
		if (decimal.Compare(v, hi) > 0)
		{
			return hi;
		}
		return v;
	}

	private void Apply_Default_Config()
	{
		Gears.Value = 4m;
		VSS.Value = 40m;
		MyProject.Forms.Lead_Form.Lead.Value = 1m;
		Ratio.W_Data(1, 1, 3.06f);
		Ratio.W_Data(1, 2, 1.63f);
		Ratio.W_Data(1, 3, 1f);
		Ratio.W_Data(1, 4, 0.7f);
		MyProject.Forms.Lead_Form.Delay.W_Data(1, 1, 0f);
		MyProject.Forms.Lead_Form.Delay.W_Data(2, 1, 0.2f);
		MyProject.Forms.Lead_Form.Delay.W_Data(1, 2, 0f);
		MyProject.Forms.Lead_Form.Delay.W_Data(2, 2, 0.3f);
		MyProject.Forms.Lead_Form.Delay.W_Data(1, 3, 0f);
		MyProject.Forms.Lead_Form.Delay.W_Data(2, 3, 0.25f);
	}

	private void Load_Presets()
	{
		TransPresets.Clear();
		SlopePresets.Clear();
		string text = Path.Combine(Application.StartupPath, "Trans_Presets.txt");
		string text2 = Path.Combine(Application.StartupPath, "Slope_Presets.txt");
		if (!File.Exists(text))
		{
			Write_Default_Trans_Presets(text);
		}
		if (!File.Exists(text2))
		{
			Write_Default_Slope_Presets(text2);
		}
		Load_Trans_Presets(text);
		Load_Slope_Presets(text2);
	}

	private void Load_Trans_Presets(string FN)
	{
		StreamReader streamReader = null;
		checked
		{
			try
			{
				streamReader = new StreamReader(FN);
				Trans_Preset item = default(Trans_Preset);
				while (!streamReader.EndOfStream)
				{
					string text = streamReader.ReadLine();
					if (text == null)
					{
						break;
					}
					text = text.Trim();
					if (Operators.CompareString(text, "", false) == 0 || text.StartsWith("#"))
					{
						continue;
					}
					string[] array = text.Split(new char[1] { '\t' });
					if (array.Length < 5 || !Versioned.IsNumeric((object)array[1]))
					{
						continue;
					}
					item.Name = array[0].Trim();
					item.Gears = (int)Math.Round(Conversion.Val(array[1]));
					item.VSS = (float)Conversion.Val(array[2]);
					item.Lead = (float)Conversion.Val(array[3]);
					item.ExportModes = ParseModes(array[4]);
					if (!((item.Gears < 2) | (item.Gears > 12)))
					{
						item.Ratios = new float[item.Gears + 1];
						item.Preps = new float[item.Gears + 1];
						item.Reacts = new float[item.Gears + 1];
						int gears = item.Gears;
						for (int i = 1; i <= gears; i++)
						{
							item.Ratios[i] = CellVal(array, 4 + i);
						}
						int num = item.Gears - 1;
						for (int j = 1; j <= num; j++)
						{
							item.Preps[j] = CellVal(array, 16 + j);
							item.Reacts[j] = CellVal(array, 28 + j);
						}
						TransPresets.Add(item);
					}
				}
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2 = ex;
				ProjectData.ClearProjectError();
			}
			finally
			{
				streamReader?.Close();
			}
		}
	}

	private float CellVal(string[] f, int idx)
	{
		if ((idx < 0) | (idx >= f.Length))
		{
			return 0f;
		}
		string text = f[idx].Trim().Trim(new char[1] { '"' });
		if (Operators.CompareString(text, "", false) == 0)
		{
			return 0f;
		}
		if (string.Compare(text, "null", ignoreCase: true) == 0)
		{
			return 0f;
		}
		return (float)Conversion.Val(text);
	}

	private int[] ParseModes(string cell)
	{
		string text = "";
		if (cell != null)
		{
			text = cell.Trim().Trim(new char[1] { '"' });
		}
		if (Operators.CompareString(text, "", false) == 0 || string.Compare(text, "null", ignoreCase: true) == 0)
		{
			return new int[0];
		}
		string[] array = text.Split(new char[1] { ',' });
		List<int> list = new List<int>();
		checked
		{
			int num = array.Length - 1;
			for (int i = 0; i <= num; i++)
			{
				string text2 = array[i].Trim().Trim(new char[1] { '"' });
				if (Operators.CompareString(text2, "", false) != 0)
				{
					list.Add((int)Math.Round(Conversion.Val(text2)));
				}
			}
			return list.ToArray();
		}
	}

	private void Load_Slope_Presets(string FN)
	{
		StreamReader streamReader = null;
		try
		{
			streamReader = new StreamReader(FN);
			Slope_Preset item = default(Slope_Preset);
			while (!streamReader.EndOfStream)
			{
				string text = streamReader.ReadLine();
				if (text == null)
				{
					break;
				}
				text = text.Trim();
				if (Operators.CompareString(text, "", false) == 0 || text.StartsWith("#"))
				{
					continue;
				}
				string[] array = text.Split(new char[1] { '\t' });
				if (array.Length >= 5 && Versioned.IsNumeric((object)array[1]))
				{
					item.Name = array[0].Trim();
					if (Operators.CompareString(item.Name, "", false) != 0)
					{
						item.Factor = (float)Conversion.Val(array[1]);
						item.Offset = (float)Conversion.Val(array[2]);
						item.UpF = (float)Conversion.Val(array[3]);
						item.DownF = (float)Conversion.Val(array[4]);
						SlopePresets.Add(item);
					}
				}
			}
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			ProjectData.ClearProjectError();
		}
		finally
		{
			streamReader?.Close();
		}
	}

	private void Write_Default_Trans_Presets(string FN)
	{
		StreamWriter streamWriter = null;
		checked
		{
			try
			{
				streamWriter = new StreamWriter(FN, append: false);
				streamWriter.WriteLine("# BC Trans - Transmission presets (tab delimited, open in Excel). The legend row below and any # lines are ignored on load.");
				streamWriter.WriteLine("# 12 columns each for Ratio / Prep / React - unused positions are 'null'.");
				streamWriter.WriteLine("# ExportMode = comma-separated list of allowed export-format combo indexes (0 = None). The current pick is kept if it's in the list, otherwise the first listed is selected. 'null' = leave unchanged. Empty this file for Custom-only.");
				string text = "Name\tGears\tVSS\tLead\tExportMode";
				int num = 1;
				do
				{
					text = text + "\tRatio" + Conversions.ToString(num);
					num++;
				}
				while (num <= 12);
				int num2 = 1;
				do
				{
					text = text + "\tPrep" + Conversions.ToString(num2);
					num2++;
				}
				while (num2 <= 12);
				int num3 = 1;
				do
				{
					text = text + "\tReact" + Conversions.ToString(num3);
					num3++;
				}
				while (num3 <= 12);
				streamWriter.WriteLine(text);
				Write_Trans_Line(streamWriter, "4L60/65/70", 4, 40f, 1f, "1,2", new float[4] { 3.06f, 1.63f, 1f, 0.7f }, new float[3] { 0f, 0f, 0f }, new float[3] { 0.35f, 0.4f, 0.35f });
				Write_Trans_Line(streamWriter, "4L80/85", 4, 40f, 1f, "1,2", new float[4] { 2.48f, 1.48f, 1f, 0.75f }, new float[3] { 0f, 0f, 0f }, new float[3] { 0.45f, 0.45f, 0.4f });
				Write_Trans_Line(streamWriter, "6L80/90", 6, 36f, 2.5f, "3,4", new float[6] { 4.03f, 2.36f, 1.53f, 1.15f, 0.85f, 0.67f }, new float[5] { 0.45f, 0.45f, 0.5f, 0.45f, 0.45f }, new float[5] { 0.15f, 0.15f, 0.15f, 0.15f, 0.15f });
				Write_Trans_Line(streamWriter, "8L90", 8, 68f, 2.5f, "5,6", new float[8] { 4.56f, 2.97f, 2.08f, 1.69f, 1.27f, 1f, 0.85f, 0.65f }, new float[7] { 0.45f, 0.35f, 0.4f, 0.4f, 0.4f, 0.4f, 0.4f }, new float[7] { 0.15f, 0.1f, 0.1f, 0.1f, 0.1f, 0.1f, 0.1f });
				Write_Trans_Line(streamWriter, "10L90", 10, 68f, 2.5f, "7", new float[10] { 4.69f, 2.98f, 2.14f, 1.76f, 1.52f, 1.27f, 1f, 0.85f, 0.68f, 0.63f }, new float[9] { 0.45f, 0.4f, 0.4f, 0.4f, 0.4f, 0.4f, 0.4f, 0.4f, 0.4f }, new float[9] { 0.15f, 0.1f, 0.1f, 0.1f, 0.1f, 0.1f, 0.1f, 0.1f, 0.1f });
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2 = ex;
				ProjectData.ClearProjectError();
			}
			finally
			{
				streamWriter?.Close();
			}
		}
	}

	private void Write_Trans_Line(StreamWriter sw, string nm, int gears, float vss, float lead, string em, float[] r, float[] p, float[] rt)
	{
		string text = nm + "\t" + Conversions.ToString(gears) + "\t" + Conversions.ToString(vss) + "\t" + Conversions.ToString(lead) + "\t" + em;
		text += PadGroup(r, 12);
		text += PadGroup(p, 12);
		text += PadGroup(rt, 12);
		sw.WriteLine(text);
	}

	private string PadGroup(float[] a, int n)
	{
		string text = "";
		checked
		{
			int num = n - 1;
			for (int i = 0; i <= num; i++)
			{
				text = ((i >= a.Length) ? (text + "\tnull") : (text + "\t" + Conversions.ToString(a[i])));
			}
			return text;
		}
	}

	private void Write_Default_Slope_Presets(string FN)
	{
		StreamWriter streamWriter = null;
		try
		{
			streamWriter = new StreamWriter(FN, append: false);
			streamWriter.WriteLine("# BC Trans - Throttle / shift-slope presets (tab delimited, open in Excel). The legend row below and any # lines are ignored on load.");
			streamWriter.WriteLine("# Empty this file for Custom-only.");
			streamWriter.WriteLine("Name\tFactor\tOffset\tUp\tDown");
			Write_Slope_Line(streamWriter, "78-85mm Cable TB", 1.35f, 0f, 5f, 5f);
			Write_Slope_Line(streamWriter, "90-105mm Cable TB", 1.25f, -5f, 5f, 5f);
			Write_Slope_Line(streamWriter, "97-04 C5 Corvette", 1.3f, 0f, 5f, 5f);
			Write_Slope_Line(streamWriter, "05-13 C6 Corvette", 1.3f, 10f, 5f, 5f);
			Write_Slope_Line(streamWriter, "05-06 GTO", 1.3f, 0f, 5f, 5f);
			Write_Slope_Line(streamWriter, "08-09 G8 / 09-15 CTSV", 1f, 3f, 3f, 5f);
			Write_Slope_Line(streamWriter, "10-15 5th Gen Camaro", 1.1f, 6f, 5f, 7f);
			Write_Slope_Line(streamWriter, "02-03 GMT800", 1.25f, 8f, 7f, 6f);
			Write_Slope_Line(streamWriter, "04-07 GMT800 / 07-13 GMT900", 1.1f, 13f, 7f, 7f);
			Write_Slope_Line(streamWriter, "11-17 Caprice /14-17 SS", 1.1f, 9f, 6f, 5f);
			Write_Slope_Line(streamWriter, "14-19 C7 Corvette", 1.05f, 12f, 8f, 7f);
			Write_Slope_Line(streamWriter, "16-24 6th Gen Camaro", 1.1f, 12f, 8f, 8f);
			Write_Slope_Line(streamWriter, "14-18 K2XX / 19-25 T1XX", 1f, 3f, 7f, 9f);
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			ProjectData.ClearProjectError();
		}
		finally
		{
			streamWriter?.Close();
		}
	}

	private void Write_Slope_Line(StreamWriter sw, string nm, float fac, float off, float up, float dn)
	{
		sw.WriteLine(nm + "\t" + Conversions.ToString(fac) + "\t" + Conversions.ToString(off) + "\t" + Conversions.ToString(up) + "\t" + Conversions.ToString(dn));
	}

	private void Gears_ValueChanged(object sender, EventArgs e)
	{
		if (Init >= 1)
		{
			ComboBox1.SelectedIndex = 0;
			MinLck.Maximum = decimal.Add(Gears.Value, 1m);
			if (decimal.Compare(MinLck.Value, Gears.Value) > 0)
			{
				AclLck.Maximum = MinLck.Value;
				AclLck.Minimum = MinLck.Value;
			}
			else
			{
				AclLck.Maximum = Gears.Value;
				AclLck.Minimum = MinLck.Value;
			}
			WotLck.Maximum = decimal.Add(Gears.Value, 1m);
			if (decimal.Compare(Gears.Value, 4m) <= 0)
			{
				Dis_High = 255;
				Dis_Low = 254;
			}
			else
			{
				Dis_High = 318;
				Dis_Low = 317;
			}
			Setup_Tables();
		}
	}

	private void VSS_ValueChanged(object sender, EventArgs e)
	{
		if (Init > 1)
		{
			ComboBox1.SelectedIndex = 0;
		}
		checked
		{
			US++;
		}
	}

	private void Ratio_click(object sender, EventArgs e)
	{
		if (Init > 1)
		{
			ComboBox1.SelectedIndex = 0;
		}
		checked
		{
			US++;
		}
	}

	private void Gear_ValueChanged(object sender, EventArgs e)
	{
		checked
		{
			US++;
		}
	}

	private void TireVisible_ValueChanged(object sender, EventArgs e)
	{
		if (Metric.Checked)
		{
			Tire.Value = new decimal(Convert.ToDouble(TireVisible.Value) / 25.4);
		}
		else
		{
			Tire.Value = TireVisible.Value;
		}
		if (!MyProject.Forms.Export_Form.CheckBox17.Checked)
		{
			MyProject.Forms.Export_Form.NDTire.Value = TireVisible.Value;
		}
		checked
		{
			US++;
		}
	}

	private void Tire_ValueChanged(object sender, EventArgs e)
	{
		if (Metric.Checked)
		{
			TireVisible.Value = new decimal(Convert.ToDouble(Tire.Value) * 25.4);
		}
		else
		{
			TireVisible.Value = Tire.Value;
		}
		checked
		{
			US++;
		}
	}

	private void Idle_ValueChanged(object sender, EventArgs e)
	{
		checked
		{
			US++;
		}
	}

	private void DRPM_ValueChanged(object sender, EventArgs e)
	{
		checked
		{
			US++;
		}
	}

	private void Stall_ValueChanged(object sender, EventArgs e)
	{
		checked
		{
			US++;
		}
	}

	private void MinLck_ValueChanged(object sender, EventArgs e)
	{
		checked
		{
			if (Init >= 1)
			{
				if (decimal.Compare(MinLck.Value, Gears.Value) > 0)
				{
					AclLck.Maximum = MinLck.Value;
					AclLck.Minimum = MinLck.Value;
				}
				else
				{
					AclLck.Maximum = Gears.Value;
					AclLck.Minimum = MinLck.Value;
				}
				US++;
			}
		}
	}

	private void AclLck_ValueChanged(object sender, EventArgs e)
	{
		checked
		{
			US++;
		}
	}

	private void WotLck_ValueChanged(object sender, EventArgs e)
	{
		checked
		{
			US++;
		}
	}

	private void Factor_ValueChanged(object sender, EventArgs e)
	{
		if (Init > 1)
		{
			ComboBox2.SelectedIndex = 0;
		}
		Update_Slope();
	}

	private void Offset_ValueChanged(object sender, EventArgs e)
	{
		if (Init > 1)
		{
			ComboBox2.SelectedIndex = 0;
		}
		Update_Slope();
	}

	private void UpF_ValueChanged(object sender, EventArgs e)
	{
		if (Init > 1)
		{
			ComboBox2.SelectedIndex = 0;
		}
		Update_Slope();
	}

	private void DownF_ValueChanged(object sender, EventArgs e)
	{
		if (Init > 1)
		{
			ComboBox2.SelectedIndex = 0;
		}
		Update_Slope();
	}

	private void Lead_Button_Click(object sender, EventArgs e)
	{
		((Control)MyProject.Forms.Lead_Form).Show();
		((Form)MyProject.Forms.Lead_Form).WindowState = (FormWindowState)0;
		((Control)MyProject.Forms.Lead_Form).Focus();
	}

	private void TCC_Button_Click(object sender, EventArgs e)
	{
		((Control)MyProject.Forms.TCC_Form).Show();
		((Form)MyProject.Forms.TCC_Form).WindowState = (FormWindowState)0;
		((Control)MyProject.Forms.TCC_Form).Focus();
	}

	private void OverRide_Button_Click(object sender, EventArgs e)
	{
		((Control)MyProject.Forms.OverRide_Form).Show();
		((Form)MyProject.Forms.OverRide_Form).WindowState = (FormWindowState)0;
		((Control)MyProject.Forms.OverRide_Form).Focus();
	}

	private void OverRideReset_Button_Click(object sender, EventArgs e)
	{
		checked
		{
			if (Init >= 1)
			{
				OverRide_Reset();
				US++;
			}
		}
	}

	private void OverRide_Enable_CheckedChanged(object sender, EventArgs e)
	{
		if (Init < 1)
		{
			return;
		}
		OverRide_LockSlope();
		if (OverRide_Enable.Checked)
		{
			((Control)Slope).Visible = false;
			((Control)Slope).Enabled = false;
			((Control)Label6).Visible = false;
			((Control)Label7).Visible = false;
			((Control)Label8).Visible = false;
			if (OverRide_Is_Zero())
			{
				OverRide_Reset();
			}
		}
		else
		{
			((Control)Slope).Visible = true;
			((Control)Slope).Enabled = true;
			((Control)Label6).Visible = true;
			((Control)Label7).Visible = true;
			((Control)Label8).Visible = true;
			((Control)MyProject.Forms.OverRide_Form).Hide();
			if (OverRide_Matches_Slope())
			{
				OverRide_Zero();
			}
		}
		checked
		{
			US++;
		}
	}

	private void OverRide_LockSlope()
	{
		bool enabled = !OverRide_Enable.Checked;
		((Control)ComboBox2).Enabled = enabled;
		((Control)Factor).Enabled = enabled;
		((Control)Offset).Enabled = enabled;
		((Control)UpF).Enabled = enabled;
		((Control)DownF).Enabled = enabled;
	}

	private void OverRide_Reset()
	{
		decimal num = decimal.Subtract(Gears.Value, 1m);
		decimal num2 = 1m;
		checked
		{
			while (ForLoopControl.ForNextCheckDec(num2, num, 1m))
			{
				int grid_X = Slope.Grid_X;
				for (int i = 1; i <= grid_X; i++)
				{
					MyProject.Forms.OverRide_Form.OverRide_Grid.W_Data((byte)i, Convert.ToByte(decimal.Subtract(decimal.Multiply(num2, 2m), 1m)), Slope.R_Data((byte)i, 2));
					MyProject.Forms.OverRide_Form.OverRide_Grid.W_Data((byte)i, Convert.ToByte(decimal.Multiply(num2, 2m)), Slope.R_Data((byte)i, 3));
				}
				num2 = decimal.Add(num2, 1m);
			}
		}
	}

	private void OverRide_Zero()
	{
		int grid_Y = MyProject.Forms.OverRide_Form.OverRide_Grid.Grid_Y;
		checked
		{
			for (int i = 1; i <= grid_Y; i++)
			{
				int grid_X = MyProject.Forms.OverRide_Form.OverRide_Grid.Grid_X;
				for (int j = 1; j <= grid_X; j++)
				{
					MyProject.Forms.OverRide_Form.OverRide_Grid.W_Data((byte)j, (byte)i, 0f);
				}
			}
		}
	}

	private bool OverRide_Is_Zero()
	{
		int grid_Y = MyProject.Forms.OverRide_Form.OverRide_Grid.Grid_Y;
		checked
		{
			for (int i = 1; i <= grid_Y; i++)
			{
				int grid_X = MyProject.Forms.OverRide_Form.OverRide_Grid.Grid_X;
				for (int j = 1; j <= grid_X; j++)
				{
					if (MyProject.Forms.OverRide_Form.OverRide_Grid.R_Data((byte)j, (byte)i) != 0f)
					{
						return false;
					}
				}
			}
			return true;
		}
	}

	private bool OverRide_Matches_Slope()
	{
		decimal num = decimal.Subtract(Gears.Value, 1m);
		decimal num2 = 1m;
		checked
		{
			while (ForLoopControl.ForNextCheckDec(num2, num, 1m))
			{
				int grid_X = Slope.Grid_X;
				for (int i = 1; i <= grid_X; i++)
				{
					if (MyProject.Forms.OverRide_Form.OverRide_Grid.R_Data((byte)i, Convert.ToByte(decimal.Subtract(decimal.Multiply(num2, 2m), 1m))) != Slope.R_Data((byte)i, 2))
					{
						return false;
					}
					if (MyProject.Forms.OverRide_Form.OverRide_Grid.R_Data((byte)i, Convert.ToByte(decimal.Multiply(num2, 2m))) != Slope.R_Data((byte)i, 3))
					{
						return false;
					}
				}
				num2 = decimal.Add(num2, 1m);
			}
			return true;
		}
	}

	private void OverRide_Capture()
	{
		float num = 0f;
		float num2 = 0f;
		int num3 = 0;
		bool flag = false;
		int grid_Y = U_Shift.Grid_Y;
		checked
		{
			for (int i = 1; i <= grid_Y; i++)
			{
				int grid_X = U_Shift.Grid_X;
				for (int j = 1; j <= grid_X; j++)
				{
					num3 = j + i * (U_Shift.Grid_X + 1);
					if ((U_Shift.SData[num3] & 8) == 0)
					{
						continue;
					}
					U_Shift.SData[num3] = (byte)(U_Shift.SData[num3] & -9);
					num = (float)((double)(Speed.R_Data(1, (byte)i) - MinSpeed[i]) - Conversion.Val(((ToolStripControlHost)Shift_Spread).Text));
					if (num > 0f)
					{
						num2 = (float)(((double)(U_Shift.R_Data((byte)j, (byte)i) - MinSpeed[i]) - Conversion.Val(((ToolStripControlHost)Shift_Spread).Text)) / (double)num);
						if (num2 < 0f)
						{
							num2 = 0f;
						}
						if (num2 > 1f)
						{
							num2 = 1f;
						}
						MyProject.Forms.OverRide_Form.OverRide_Grid.W_Data((byte)j, (byte)(i * 2 - 1), num2);
						flag = true;
					}
				}
			}
			int grid_Y2 = D_Shift.Grid_Y;
			for (int k = 1; k <= grid_Y2; k++)
			{
				int grid_X2 = D_Shift.Grid_X;
				for (int l = 1; l <= grid_X2; l++)
				{
					num3 = l + k * (D_Shift.Grid_X + 1);
					if ((D_Shift.SData[num3] & 8) == 0)
					{
						continue;
					}
					D_Shift.SData[num3] = (byte)(D_Shift.SData[num3] & -9);
					num = Speed.R_Data(4, (byte)k) - MinSpeed[k];
					if (num > 0f)
					{
						num2 = (D_Shift.R_Data((byte)l, (byte)k) - MinSpeed[k]) / num;
						if (num2 < 0f)
						{
							num2 = 0f;
						}
						if (num2 > 1f)
						{
							num2 = 1f;
						}
						MyProject.Forms.OverRide_Form.OverRide_Grid.W_Data((byte)l, (byte)(k * 2), num2);
						flag = true;
					}
				}
			}
			if (flag)
			{
				US++;
			}
		}
	}

	private void Setup_Tables()
	{
		if (Init < 1)
		{
			return;
		}
		Ratio.Grid_Y = Convert.ToInt32(Gears.Value);
		int grid_Y = Ratio.Grid_Y;
		checked
		{
			for (int i = 1; i <= grid_Y; i++)
			{
				if (Ratio.R_Data(1, (byte)i) <= 0f)
				{
					Ratio.W_Data(1, (byte)i, 1f);
				}
			}
			((Control)GroupBox2).Height = ((Control)Ratio).Height + 42;
			if (((Control)GroupBox2).Height < 120)
			{
				((Control)GroupBox2).Height = 120;
			}
			Speed.Grid_Y = Convert.ToInt32(Gears.Value);
			((Control)GroupBox4).Height = ((Control)GroupBox2).Height;
			RPM.Grid_Y = Convert.ToInt32(Gears.Value);
			int grid_Y2 = RPM.Grid_Y;
			for (int j = 1; j <= grid_Y2; j++)
			{
				if (RPM.R_Data(1, (byte)j) <= 0f)
				{
					if (j == 1)
					{
						RPM.W_Data(1, (byte)j, 5900f);
					}
					else if (RPM.R_Data(1, (byte)(j - 1)) > 1000f)
					{
						RPM.W_Data(1, (byte)j, RPM.R_Data(1, (byte)(j - 1)));
					}
					else
					{
						RPM.W_Data(1, (byte)j, 5900f);
					}
				}
			}
			((Control)GroupBox5).Height = ((Control)GroupBox2).Height;
			((Control)GroupBox6).Height = ((Control)GroupBox2).Height;
			((Control)GroupBox3).Top = ((Control)GroupBox2).Top + ((Control)GroupBox2).Height + 7;
			((Control)GroupBox1).Top = ((Control)GroupBox3).Top + ((Control)GroupBox3).Height + 7;
			U_Shift.Grid_Y = Convert.ToInt32(decimal.Subtract(Gears.Value, 1m));
			int grid_Y3 = U_Shift.Grid_Y;
			for (int k = 1; k <= grid_Y3; k++)
			{
				U_Shift.W_Data(0, (byte)k, k + 1);
			}
			D_Shift.Grid_Y = Convert.ToInt32(decimal.Subtract(Gears.Value, 1m));
			int grid_Y4 = D_Shift.Grid_Y;
			for (int l = 1; l <= grid_Y4; l++)
			{
				D_Shift.W_Data(0, (byte)l, l);
			}
			Lock.Grid_Y = Convert.ToInt32(Gears.Value);
			int grid_Y5 = Lock.Grid_Y;
			for (int m = 1; m <= grid_Y5; m++)
			{
				Lock.W_Data(0, (byte)m, m);
			}
			Unlock.Grid_Y = Convert.ToInt32(Gears.Value);
			int grid_Y6 = Unlock.Grid_Y;
			for (int n = 1; n <= grid_Y6; n++)
			{
				Unlock.W_Data(0, (byte)n, n);
			}
			int num = U_Shift.Grid_X - 1;
			for (int num2 = 1; num2 <= num; num2++)
			{
				U_Shift.W_Data((byte)(num2 + 1), 0, (float)(6.25 * (double)num2));
				D_Shift.W_Data((byte)(num2 + 1), 0, (float)(6.25 * (double)num2));
				Lock.W_Data((byte)(num2 + 1), 0, (float)(6.25 * (double)num2));
				Unlock.W_Data((byte)(num2 + 1), 0, (float)(6.25 * (double)num2));
				MyProject.Forms.TCC_Form.MinTCC.W_Data((byte)(num2 + 1), 0, (float)(6.25 * (double)num2));
				MyProject.Forms.OverRide_Form.OverRide_Grid.W_Data((byte)(num2 + 1), 0, (float)(6.25 * (double)num2));
			}
			((Control)D_Shift).Left = ((Control)U_Shift).Left;
			((Control)D_Shift).Top = ((Control)U_Shift).Top + ((Control)U_Shift).Height + 5;
			((Control)Lock).Left = ((Control)D_Shift).Left;
			((Control)Lock).Top = ((Control)D_Shift).Top + ((Control)D_Shift).Height + 5;
			((Control)Unlock).Left = ((Control)Lock).Left;
			((Control)Unlock).Top = ((Control)Lock).Top + ((Control)Lock).Height + 5;
			((Control)GroupBox1).Height = ((Control)Unlock).Top + ((Control)Unlock).Height + 10;
			((Control)this).Height = ((Control)GroupBox1).Top + ((Control)GroupBox1).Height + 42;
			MyProject.Forms.Lead_Form.Delay.Grid_Y = Convert.ToInt32(decimal.Subtract(Gears.Value, 1m));
			int grid_Y7 = MyProject.Forms.Lead_Form.Delay.Grid_Y;
			for (int num3 = 1; num3 <= grid_Y7; num3++)
			{
				if (MyProject.Forms.Lead_Form.Delay.R_Data(1, (byte)num3) <= 0f)
				{
					MyProject.Forms.Lead_Form.Delay.W_Data(1, (byte)num3, 0f);
				}
				MyProject.Forms.Lead_Form.Delay.W_Data(0, (byte)num3, num3 + 1);
			}
			MyProject.Forms.TCC_Form.MinTCC.Grid_Y = Convert.ToInt32(decimal.Multiply(Gears.Value, 2m));
			decimal value = Gears.Value;
			decimal num4 = 1m;
			while (ForLoopControl.ForNextCheckDec(num4, value, 1m))
			{
				MyProject.Forms.TCC_Form.MinTCC.W_Data(0, Convert.ToByte(decimal.Subtract(decimal.Multiply(num4, 2m), 1m)), Convert.ToSingle(num4));
				MyProject.Forms.TCC_Form.MinTCC.W_Data(0, Convert.ToByte(decimal.Multiply(num4, 2m)), Convert.ToSingle(num4));
				if (decimal.Compare(num4, 1m) > 0)
				{
					int grid_X = MyProject.Forms.TCC_Form.MinTCC.Grid_X;
					for (int num5 = 1; num5 <= grid_X; num5++)
					{
						if (MyProject.Forms.TCC_Form.MinTCC.R_Data((byte)num5, Convert.ToByte(decimal.Subtract(decimal.Multiply(num4, 2m), 1m))) == 0f)
						{
							MyProject.Forms.TCC_Form.MinTCC.W_Data((byte)num5, Convert.ToByte(decimal.Subtract(decimal.Multiply(num4, 2m), 1m)), MyProject.Forms.TCC_Form.MinTCC.R_Data((byte)num5, Convert.ToByte(decimal.Subtract(decimal.Multiply(decimal.Subtract(num4, 1m), 2m), 1m))));
							MyProject.Forms.TCC_Form.MinTCC.W_Data((byte)num5, Convert.ToByte(decimal.Multiply(num4, 2m)), MyProject.Forms.TCC_Form.MinTCC.R_Data((byte)num5, Convert.ToByte(decimal.Multiply(decimal.Subtract(num4, 1m), 2m))));
						}
					}
				}
				num4 = decimal.Add(num4, 1m);
			}
			((Control)MyProject.Forms.TCC_Form.GroupBox1).Height = ((Control)MyProject.Forms.TCC_Form.MinTCC).Height + 31;
			((Control)MyProject.Forms.TCC_Form).Height = ((Control)MyProject.Forms.TCC_Form.GroupBox1).Height + 150;
			MyProject.Forms.OverRide_Form.OverRide_Grid.Grid_Y = Convert.ToInt32(decimal.Multiply(decimal.Subtract(Gears.Value, 1m), 2m));
			decimal num6 = decimal.Subtract(Gears.Value, 1m);
			decimal num7 = 1m;
			while (ForLoopControl.ForNextCheckDec(num7, num6, 1m))
			{
				MyProject.Forms.OverRide_Form.OverRide_Grid.W_Data(0, Convert.ToByte(decimal.Subtract(decimal.Multiply(num7, 2m), 1m)), Convert.ToSingle(decimal.Add(num7, 1m)));
				MyProject.Forms.OverRide_Form.OverRide_Grid.W_Data(0, Convert.ToByte(decimal.Multiply(num7, 2m)), Convert.ToSingle(num7));
				if (decimal.Compare(num7, 1m) > 0)
				{
					int grid_X2 = MyProject.Forms.OverRide_Form.OverRide_Grid.Grid_X;
					for (int num8 = 1; num8 <= grid_X2; num8++)
					{
						if (MyProject.Forms.OverRide_Form.OverRide_Grid.R_Data((byte)num8, Convert.ToByte(decimal.Subtract(decimal.Multiply(num7, 2m), 1m))) == 0f)
						{
							MyProject.Forms.OverRide_Form.OverRide_Grid.W_Data((byte)num8, Convert.ToByte(decimal.Subtract(decimal.Multiply(num7, 2m), 1m)), MyProject.Forms.OverRide_Form.OverRide_Grid.R_Data((byte)num8, Convert.ToByte(decimal.Subtract(decimal.Multiply(decimal.Subtract(num7, 1m), 2m), 1m))));
							MyProject.Forms.OverRide_Form.OverRide_Grid.W_Data((byte)num8, Convert.ToByte(decimal.Multiply(num7, 2m)), MyProject.Forms.OverRide_Form.OverRide_Grid.R_Data((byte)num8, Convert.ToByte(decimal.Multiply(decimal.Subtract(num7, 1m), 2m))));
						}
					}
				}
				num7 = decimal.Add(num7, 1m);
			}
			((Control)MyProject.Forms.OverRide_Form.GroupBox1).Height = ((Control)MyProject.Forms.OverRide_Form.OverRide_Grid).Height + 31;
			((Control)MyProject.Forms.OverRide_Form).Height = ((Control)MyProject.Forms.OverRide_Form.GroupBox1).Height + 53;
			US++;
		}
	}

	public void Update_Slope()
	{
		if (Init < 1)
		{
			return;
		}
		float num = 0f;
		float[] array = new float[17]
		{
			0f, 0.1f, 0.1f, 0.1f, 0.1f, 0.125f, 0.15f, 0.225f, 0.35f, 0.5f,
			0.675f, 0.825f, 0.925f, 0.95f, 1f, 1f, 1f
		};
		Slope.W_Data(1, 1, 0f);
		int grid_X = Slope.Grid_X;
		checked
		{
			for (int i = 2; i <= grid_X; i++)
			{
				num = U_Shift.R_Data((byte)i, 0);
				num -= Convert.ToSingle(Offset.Value);
				if (num < 0f)
				{
					num = 0f;
				}
				if (num > 100f)
				{
					num = 100f;
				}
				num /= 100f;
				num = (float)Math.Pow(num, Convert.ToDouble(Factor.Value));
				if (num < 0f)
				{
					num = 0f;
				}
				if (num > 1f)
				{
					num = 1f;
				}
				Slope.W_Data((byte)i, 1, num);
			}
			Slope.W_Data((byte)Slope.Grid_X, 1, 1f);
			Slope.W_Data(1, 2, 0f);
			int grid_X2 = Slope.Grid_X;
			for (int j = 2; j <= grid_X2; j++)
			{
				num = U_Shift.R_Data((byte)j, 0);
				num -= Convert.ToSingle(Offset.Value);
				if (num < 0f)
				{
					num = 0f;
				}
				if (num > 100f)
				{
					num = 100f;
				}
				num /= 100f;
				num = (float)(1.0 - Math.Pow(1f - num, Convert.ToDouble(decimal.Add(Factor.Value, decimal.Divide(UpF.Value, 10m)))));
				num = Slope.R_Data((byte)j, 1) + (num - Slope.R_Data((byte)j, 1)) * array[j - 1];
				if (num < 0f)
				{
					num = 0f;
				}
				if (num > 1f)
				{
					num = 1f;
				}
				Slope.W_Data((byte)j, 2, num);
			}
			Slope.W_Data((byte)Slope.Grid_X, 2, 1f);
			Slope.W_Data(1, 3, 0f);
			int grid_X3 = Slope.Grid_X;
			for (int k = 2; k <= grid_X3; k++)
			{
				num = U_Shift.R_Data((byte)k, 0);
				num -= Convert.ToSingle(Offset.Value);
				if (num < 0f)
				{
					num = 0f;
				}
				if (num > 100f)
				{
					num = 100f;
				}
				num /= 100f;
				num = (float)Math.Pow(num, Convert.ToDouble(Factor.Value) + 0.1 + Convert.ToDouble(decimal.Divide(decimal.Subtract(10m, DownF.Value), 5m)));
				if (num < 0f)
				{
					num = 0f;
				}
				if (num > 1f)
				{
					num = 1f;
				}
				Slope.W_Data((byte)k, 3, num);
			}
			Slope.W_Data((byte)Slope.Grid_X, 3, 1f);
			US++;
		}
	}

	public void Calc_Shifts()
	{
		if (Init < 1)
		{
			return;
		}
		long num = 0L;
		float num2 = 0f;
		float num3 = 0f;
		float num4 = 0f;
		float num5 = 0f;
		int grid_Y = RPM.Grid_Y;
		checked
		{
			for (int i = 1; i <= grid_Y; i++)
			{
				if (RPM.R_Data(1, (byte)i) <= 0f)
				{
					RPM.W_Data(1, (byte)i, 5000f);
				}
				if (RPM.R_Data(1, (byte)i) < 1500f)
				{
					RPM.W_Data(1, (byte)i, 1500f);
				}
			}
			Stall_Slip = (float)(Math.Pow(Convert.ToDouble(decimal.Divide(Stall.Value, 1000m)), 1.7) / 100.0);
			decimal value = Gears.Value;
			decimal num6 = 1m;
			while (ForLoopControl.ForNextCheckDec(num6, value, 1m))
			{
				MinSpeed[Convert.ToInt32(num6)] = (float)((double)(Convert.ToSingle(decimal.Add(Idle.Value, 400m)) / (Ratio.R_Data(1, Convert.ToByte(num6)) * Convert.ToSingle(Gear.Value))) * (Convert.ToDouble(Tire.Value) * 3.14) * 60.0 / 12.0 / 5280.0);
				num6 = decimal.Add(num6, 1m);
			}
			int grid_Y2 = Lock.Grid_Y;
			for (int j = 1; j <= grid_Y2; j++)
			{
				int grid_X = Lock.Grid_X;
				for (int k = 1; k <= grid_X; k++)
				{
					MinTCCSpeed[k, j] = (float)((double)(MyProject.Forms.TCC_Form.MinTCC.R_Data((byte)k, (byte)(j * 2 - 1)) / (Ratio.R_Data(1, (byte)j) * Convert.ToSingle(Gear.Value))) * (Convert.ToDouble(Tire.Value) * 3.14) * 60.0 / 12.0 / 5280.0);
				}
			}
			int grid_X2 = Slope.Grid_X;
			for (int l = 1; l <= grid_X2; l++)
			{
				num3 = StallBase[l - 1] + Slope.R_Data((byte)l, 1);
				if ((double)num3 > 0.66)
				{
					num3 = 0.66f;
				}
				StallMin[l] = num3 * Convert.ToSingle(Stall.Value) + Convert.ToSingle(Idle.Value);
				if (Operators.ConditionalCompareObjectGreater(StallMin[l], (object)Stall.Value, false))
				{
					StallMin[l] = Stall.Value;
				}
			}
			int grid_Y3 = Speed.Grid_Y;
			for (int m = 1; m <= grid_Y3; m++)
			{
				Speed.W_Data(1, (byte)m, (float)((double)(RPM.R_Data(1, (byte)m) / (Ratio.R_Data(1, (byte)m) * Convert.ToSingle(Gear.Value))) * (Convert.ToDouble(Tire.Value) * 3.14) * 60.0 / 12.0 / 5280.0));
				Speed.W_Data(2, (byte)m, Speed.R_Data(1, (byte)m) * (1f - Stall_Slip));
				num3 = ((!MaxSpeed_Locked.Checked) ? Speed.R_Data(2, (byte)m) : ((decimal.Compare(new decimal(m), WotLck.Value) < 0) ? Speed.R_Data(2, (byte)m) : Speed.R_Data(1, (byte)m)));
				if (MyProject.Forms.Lead_Form.Lead_Radio1.Checked)
				{
					Speed.W_Data(3, (byte)m, (float)((double)num3 * (1.0 - 0.01 * (double)Ratio.R_Data(1, (byte)m) * Convert.ToDouble(Gear.Value) * Convert.ToDouble(decimal.Divide(MyProject.Forms.Lead_Form.Lead.Value, 8m))) - (double)((Ratio.R_Data(1, (byte)m) + 1f) * Convert.ToSingle(Gear.Value) * Convert.ToSingle(decimal.Divide(MyProject.Forms.Lead_Form.Lead.Value, 8m)))));
					if ((double)Speed.R_Data(3, (byte)m) < (double)Speed.R_Data(2, (byte)m) * 0.2)
					{
						Speed.W_Data(3, (byte)m, (float)((double)Speed.R_Data(2, (byte)m) * 0.2));
					}
					Speed.W_Data(4, (byte)m, (float)((double)Speed.R_Data(3, (byte)m) * 0.98 - 2.0 - (double)(Ratio.R_Data(1, (byte)m) * Convert.ToSingle(Gear.Value) * Convert.ToSingle(decimal.Add(1m, decimal.Divide(MyProject.Forms.Lead_Form.Lead.Value, 10m)))) * 0.5));
					num3 = (float)((double)(Convert.ToSingle(DRPM.Value) / (Ratio.R_Data(1, (byte)m) * Convert.ToSingle(Gear.Value))) * (Convert.ToDouble(Tire.Value) * 3.14) * 60.0 / 12.0 / 5280.0);
					if (Speed.R_Data(4, (byte)m) > num3)
					{
						Speed.W_Data(4, (byte)m, num3);
					}
					if ((double)Speed.R_Data(4, (byte)m) < (double)Speed.R_Data(3, (byte)m) * 0.2)
					{
						Speed.W_Data(4, (byte)m, (float)((double)Speed.R_Data(3, (byte)m) * 0.2));
					}
					continue;
				}
				num2 = (float)(Convert.ToDouble(MyProject.Forms.Lead_Form.RWHP.Value) * 0.75 * 375.0 / (double)num3 / Convert.ToDouble(MyProject.Forms.Lead_Form.Weight.Value) * 21.93685);
				if (m <= MyProject.Forms.Lead_Form.Delay.Grid_Y)
				{
					Speed.W_Data(3, (byte)m, num3 - num2 * (MyProject.Forms.Lead_Form.Delay.R_Data(1, (byte)m) + MyProject.Forms.Lead_Form.Delay.R_Data(2, (byte)m)));
					Speed.W_Data(4, (byte)m, num3 - num2 * (Convert.ToSingle(MyProject.Forms.Lead_Form.Down_Time.Value) + MyProject.Forms.Lead_Form.Delay.R_Data(1, (byte)m) + MyProject.Forms.Lead_Form.Delay.R_Data(2, (byte)m)));
				}
				else
				{
					Speed.W_Data(3, (byte)m, num3 - num2 * (MyProject.Forms.Lead_Form.Delay.R_Data(1, (byte)MyProject.Forms.Lead_Form.Delay.Grid_Y) + MyProject.Forms.Lead_Form.Delay.R_Data(2, (byte)MyProject.Forms.Lead_Form.Delay.Grid_Y)));
					Speed.W_Data(4, (byte)m, num3 - num2 * (Convert.ToSingle(MyProject.Forms.Lead_Form.Down_Time.Value) + MyProject.Forms.Lead_Form.Delay.R_Data(1, (byte)MyProject.Forms.Lead_Form.Delay.Grid_Y) + MyProject.Forms.Lead_Form.Delay.R_Data(2, (byte)MyProject.Forms.Lead_Form.Delay.Grid_Y)));
				}
				num3 = (float)((double)(Convert.ToSingle(DRPM.Value) / (Ratio.R_Data(1, (byte)m) * Convert.ToSingle(Gear.Value))) * (Convert.ToDouble(Tire.Value) * 3.14) * 60.0 / 12.0 / 5280.0);
				if (Speed.R_Data(4, (byte)m) > num3)
				{
					Speed.W_Data(4, (byte)m, num3);
				}
				if ((double)Speed.R_Data(4, (byte)m) > (double)Speed.R_Data(3, (byte)m) - Conversion.Val(((ToolStripControlHost)Shift_Spread).Text))
				{
					Speed.W_Data(4, (byte)m, (float)((double)Speed.R_Data(3, (byte)m) - Conversion.Val(((ToolStripControlHost)Shift_Spread).Text)));
				}
				if ((double)Speed.R_Data(4, (byte)m) < (double)Speed.R_Data(3, (byte)m) * 0.2)
				{
					Speed.W_Data(4, (byte)m, (float)((double)Speed.R_Data(3, (byte)m) * 0.2));
				}
			}
			int grid_Y4 = U_Shift.Grid_Y;
			for (int n = 1; n <= grid_Y4; n++)
			{
				int grid_X3 = U_Shift.Grid_X;
				for (int num7 = 1; num7 <= grid_X3; num7++)
				{
					num4 = ((!OverRide_Enable.Checked) ? Slope.R_Data((byte)num7, 2) : MyProject.Forms.OverRide_Form.OverRide_Grid.R_Data((byte)num7, (byte)(n * 2 - 1)));
					U_Shift.W_Data((byte)num7, (byte)n, (float)((double)MinSpeed[n] + Conversion.Val(((ToolStripControlHost)Shift_Spread).Text) + ((double)(Speed.R_Data(1, (byte)n) - MinSpeed[n]) - Conversion.Val(((ToolStripControlHost)Shift_Spread).Text)) * (double)num4));
				}
			}
			int grid_Y5 = D_Shift.Grid_Y;
			for (int num8 = 1; num8 <= grid_Y5; num8++)
			{
				int grid_X4 = D_Shift.Grid_X;
				for (int num9 = 1; num9 <= grid_X4; num9++)
				{
					num5 = ((!OverRide_Enable.Checked) ? Slope.R_Data((byte)num9, 3) : MyProject.Forms.OverRide_Form.OverRide_Grid.R_Data((byte)num9, (byte)(num8 * 2)));
					D_Shift.W_Data((byte)num9, (byte)num8, MinSpeed[num8] + (Speed.R_Data(4, (byte)num8) - MinSpeed[num8]) * num5);
				}
			}
			int grid_Y6 = Unlock.Grid_Y;
			for (int num10 = 2; num10 <= grid_Y6; num10++)
			{
				int grid_X5 = Unlock.Grid_X;
				for (int num11 = 1; num11 <= grid_X5; num11++)
				{
					Unlock.W_Data((byte)num11, (byte)num10, (float)((double)D_Shift.R_Data((byte)num11, (byte)(num10 - 1)) + Conversion.Val(((ToolStripControlHost)Unlock_Shift_Spread).Text)));
				}
			}
			int grid_Y7 = Unlock.Grid_Y;
			for (int num12 = 1; num12 <= grid_Y7; num12++)
			{
				int grid_X6 = Unlock.Grid_X;
				for (int num13 = 1; num13 <= grid_X6; num13++)
				{
					if (num12 == 1)
					{
						Unlock.W_Data((byte)num13, (byte)num12, 0f);
					}
					if (Unlock.R_Data((byte)num13, (byte)num12) < MinTCCSpeed[num13, num12])
					{
						Unlock.W_Data((byte)num13, (byte)num12, MinTCCSpeed[num13, num12]);
					}
				}
			}
			int grid_Y8 = Lock.Grid_Y;
			for (int num14 = 1; num14 <= grid_Y8; num14++)
			{
				int grid_X7 = Lock.Grid_X;
				for (int num15 = 1; num15 <= grid_X7; num15++)
				{
					Lock.W_Data((byte)num15, (byte)num14, (float)((double)Unlock.R_Data((byte)num15, (byte)num14) + Conversion.Val(((ToolStripControlHost)Lock_Spread).Text)));
				}
			}
			if (StallLogic.Checked)
			{
				int grid_Y9 = Lock.Grid_Y;
				for (int num16 = 1; num16 <= grid_Y9; num16++)
				{
					int grid_X8 = Lock.Grid_X;
					for (int num17 = 1; num17 <= grid_X8; num17++)
					{
						num3 = Conversions.ToSingle(StallMin[num17 - 1]);
						if ((double)num3 > (double)RPM.R_Data(1, (byte)num16) * 0.66)
						{
							num3 = (float)((double)RPM.R_Data(1, (byte)num16) * 0.66);
						}
						num3 = (float)((double)(num3 / (Ratio.R_Data(1, (byte)num16) * Convert.ToSingle(Gear.Value))) * (Convert.ToDouble(Tire.Value) * 3.14) * 60.0 / 12.0 / 5280.0);
						if (num3 > Lock.R_Data((byte)num17, (byte)num16))
						{
							Lock.W_Data((byte)num17, (byte)num16, num3);
						}
					}
				}
			}
			int num18 = 1;
			do
			{
				num = 0L;
				if (num18 == 32)
				{
					U_Shift.Clear_Selected();
					D_Shift.Clear_Selected();
					Lock.Clear_Selected();
					Unlock.Clear_Selected();
				}
				if (InitLock.Checked)
				{
					int grid_Y10 = Lock.Grid_Y;
					for (int num19 = 1; num19 <= grid_Y10; num19++)
					{
						int num20 = Lock.Grid_X - 3;
						for (int num21 = 1; num21 <= num20; num21++)
						{
							if (decimal.Compare(new decimal(num19), AclLck.Value) != 0)
							{
								continue;
							}
							if (unchecked(num19 < U_Shift.Grid_Y && num19 == 1))
							{
								num3 = (float)((double)Lock.R_Data((byte)num21, (byte)num19) + Conversion.Val(((ToolStripControlHost)Lock_Shift_Spread).Text));
								if (U_Shift.R_Data((byte)num21, (byte)num19) < num3)
								{
									U_Shift.W_Data((byte)num21, (byte)num19, num3);
									num++;
									U_Shift.SData[num21 + num19 * (U_Shift.Grid_X + 1)] = 1;
								}
							}
							else if (num19 <= U_Shift.Grid_Y)
							{
								num3 = (U_Shift.R_Data((byte)num21, (byte)(num19 - 1)) + U_Shift.R_Data((byte)num21, (byte)num19)) / 2f;
								if (Lock.R_Data((byte)num21, (byte)num19) < num3)
								{
									Lock.W_Data((byte)num21, (byte)num19, num3);
									num++;
									Lock.SData[num21 + num19 * (Lock.Grid_X + 1)] = 1;
								}
								num3 = (float)((double)U_Shift.R_Data((byte)num21, (byte)(num19 - 1)) + Conversion.Val(((ToolStripControlHost)Lock_Shift_Spread).Text));
								if (Lock.R_Data((byte)num21, (byte)num19) < num3)
								{
									Lock.W_Data((byte)num21, (byte)num19, num3);
									num++;
									Lock.SData[num21 + num19 * (Lock.Grid_X + 1)] = 1;
								}
								num3 = (float)((double)Lock.R_Data((byte)num21, (byte)num19) + Conversion.Val(((ToolStripControlHost)Lock_Shift_Spread).Text));
								if (U_Shift.R_Data((byte)num21, (byte)num19) < num3)
								{
									U_Shift.W_Data((byte)num21, (byte)num19, num3);
									num++;
									U_Shift.SData[num21 + num19 * (U_Shift.Grid_X + 1)] = 1;
								}
							}
							else if (num19 > U_Shift.Grid_Y)
							{
								num3 = (float)((double)U_Shift.R_Data((byte)num21, (byte)(num19 - 1)) + Conversion.Val(((ToolStripControlHost)Lock_Shift_Spread).Text));
								if (Lock.R_Data((byte)num21, (byte)num19) < num3)
								{
									Lock.W_Data((byte)num21, (byte)num19, num3);
									num++;
									Lock.SData[num21 + num19 * (Lock.Grid_X + 1)] = 1;
								}
							}
						}
					}
				}
				if (PreLock.Checked)
				{
					for (int num22 = U_Shift.Grid_Y; num22 >= 1; num22 += -1)
					{
						int num23 = U_Shift.Grid_X - 3;
						for (int num24 = 1; num24 <= num23; num24++)
						{
							if (decimal.Compare(new decimal(num22), AclLck.Value) < 0)
							{
								num3 = (float)((double)U_Shift.R_Data((byte)num24, (byte)num22) + 2.5);
								if (Lock.R_Data((byte)num24, (byte)num22) < num3)
								{
									Lock.W_Data((byte)num24, (byte)num22, num3);
									num += 10;
									Lock.SData[num24 + num22 * (Lock.Grid_X + 1)] = 1;
								}
							}
						}
					}
				}
				if (PostLock.Checked)
				{
					int grid_Y11 = Lock.Grid_Y;
					for (int num25 = 1; num25 <= grid_Y11; num25++)
					{
						int num26 = Lock.Grid_X - 3;
						for (int num27 = 1; num27 <= num26; num27++)
						{
							if (decimal.Compare(new decimal(num25), AclLck.Value) > 0)
							{
								num3 = Lock.R_Data((byte)num27, (byte)num25) + 1f;
								if (U_Shift.R_Data((byte)num27, (byte)(num25 - 1)) < num3)
								{
									U_Shift.W_Data((byte)num27, (byte)(num25 - 1), num3);
									num += 100;
									U_Shift.SData[num27 + (num25 - 1) * (U_Shift.Grid_X + 1)] = 1;
								}
							}
						}
					}
				}
				for (int num28 = Unlock.Grid_Y; num28 >= 1; num28 += -1)
				{
					int num29 = Lock.Grid_X - 3;
					for (int num30 = 1; num30 <= num29; num30++)
					{
						if (decimal.Compare(new decimal(num28), AclLck.Value) > 0)
						{
							num3 = (float)((double)Unlock.R_Data((byte)num30, (byte)num28) + Conversion.Val(((ToolStripControlHost)Unlock_Shift_Spread).Text));
							if ((MyProject.Forms.TCC_Form.MinTCC.R_Data((byte)num30, (byte)(num28 * 2)) != 1f) & (D_Shift.R_Data((byte)num30, (byte)(num28 - 1)) < num3))
							{
								D_Shift.W_Data((byte)num30, (byte)(num28 - 1), num3);
								num += 1000;
								D_Shift.SData[num30 + (num28 - 1) * (D_Shift.Grid_X + 1)] = 1;
							}
						}
					}
				}
				if (ULckStay.Checked)
				{
					for (int num31 = Unlock.Grid_Y; num31 >= 2; num31 += -1)
					{
						int num32 = Lock.Grid_X - 3;
						for (int num33 = 1; num33 <= num32; num33++)
						{
							if (Unlock.R_Data((byte)num33, (byte)num31) > D_Shift.R_Data((byte)num33, (byte)(num31 - 1)) && Lock.R_Data((byte)num33, (byte)(num31 - 1)) < D_Shift.R_Data((byte)num33, (byte)(num31 - 1)))
							{
								Lock.W_Data((byte)num33, (byte)(num31 - 1), (float)((double)D_Shift.R_Data((byte)num33, (byte)(num31 - 1)) + Conversion.Val(((ToolStripControlHost)Unlock_Shift_Spread).Text)));
								num += 10000000;
								Lock.SData[num33 + (num31 - 1) * (Lock.Grid_X + 1)] = 1;
							}
						}
					}
				}
				if (LockUnlock.Checked)
				{
					for (int num34 = Lock.Grid_Y; num34 >= 1; num34 += -1)
					{
						int num35 = Lock.Grid_X - 3;
						for (int num36 = 1; num36 <= num35; num36++)
						{
							num3 = (float)((double)Unlock.R_Data((byte)num36, (byte)num34) + Conversion.Val(((ToolStripControlHost)Lock_Spread).Text));
							if (Lock.R_Data((byte)num36, (byte)num34) < num3)
							{
								Lock.W_Data((byte)num36, (byte)num34, num3);
								num += 10000;
								Lock.SData[num36 + num34 * (Lock.Grid_X + 1)] = 1;
							}
						}
					}
				}
				if (UpDown.Checked)
				{
					for (int num37 = U_Shift.Grid_Y; num37 >= 1; num37 += -1)
					{
						int grid_X9 = U_Shift.Grid_X;
						for (int num38 = 1; num38 <= grid_X9; num38++)
						{
							num3 = (float)((double)D_Shift.R_Data((byte)num38, (byte)num37) + Conversion.Val(((ToolStripControlHost)Shift_Spread).Text));
							if (U_Shift.R_Data((byte)num38, (byte)num37) < num3)
							{
								U_Shift.W_Data((byte)num38, (byte)num37, num3);
								num += 100000;
								U_Shift.SData[num38 + num37 * (U_Shift.Grid_X + 1)] = 1;
							}
						}
					}
				}
				if (ShiftMax.Checked)
				{
					int grid_Y12 = U_Shift.Grid_Y;
					for (int num39 = 1; num39 <= grid_Y12; num39++)
					{
						int grid_X10 = U_Shift.Grid_X;
						for (int num40 = 1; num40 <= grid_X10; num40++)
						{
							if (U_Shift.R_Data((byte)num40, (byte)num39) > Speed.R_Data(3, (byte)num39))
							{
								U_Shift.W_Data((byte)num40, (byte)num39, Speed.R_Data(3, (byte)num39));
								num += 1000000;
								U_Shift.SData[num40 + num39 * (U_Shift.Grid_X + 1)] = 1;
							}
						}
					}
					int grid_Y13 = D_Shift.Grid_Y;
					for (int num41 = 1; num41 <= grid_Y13; num41++)
					{
						int grid_X11 = D_Shift.Grid_X;
						for (int num42 = 1; num42 <= grid_X11; num42++)
						{
							if (D_Shift.R_Data((byte)num42, (byte)num41) > Speed.R_Data(4, (byte)num41))
							{
								D_Shift.W_Data((byte)num42, (byte)num41, Speed.R_Data(4, (byte)num41));
								num += 1000000;
								D_Shift.SData[num42 + num41 * (D_Shift.Grid_X + 1)] = 1;
							}
						}
					}
				}
				if (num == 0)
				{
					break;
				}
				num18++;
			}
			while (num18 <= 32);
			int grid_X12 = Unlock.Grid_X;
			for (int num43 = 1; num43 <= grid_X12; num43++)
			{
				int grid_Y14 = Unlock.Grid_Y;
				for (int num44 = 1; num44 <= grid_Y14; num44++)
				{
					if (MyProject.Forms.TCC_Form.MinTCC.R_Data((byte)num43, (byte)(num44 * 2)) == 2f)
					{
						Lock.W_Data((byte)num43, (byte)num44, Unlock.R_Data((byte)num43, (byte)num44));
					}
				}
			}
			if (MyProject.Forms.TCC_Form.CheckBox1.Checked)
			{
				MyProject.Forms.TCC_Form.WOTLockRPM.Value = 1000m;
				MyProject.Forms.TCC_Form.WOTStayLocked.Checked = false;
			}
			decimal value2 = WotLck.Value;
			decimal num45 = new decimal(Lock.Grid_Y);
			decimal num46 = value2;
			while (ForLoopControl.ForNextCheckDec(num46, num45, 1m))
			{
				num3 = ((!MaxSpeed_Locked.Checked) ? Speed.R_Data(2, Convert.ToByte(num46)) : ((decimal.Compare(num46, WotLck.Value) < 0) ? Speed.R_Data(2, Convert.ToByte(num46)) : Speed.R_Data(1, Convert.ToByte(num46))));
				num2 = (float)(Convert.ToDouble(MyProject.Forms.Lead_Form.RWHP.Value) * 0.75 * 375.0 / (double)num3 / Convert.ToDouble(MyProject.Forms.Lead_Form.Weight.Value) * 21.93685);
				int num47 = Lock.Grid_X - 2;
				int grid_X13 = Lock.Grid_X;
				for (int num48 = num47; num48 <= grid_X13; num48++)
				{
					if (MyProject.Forms.TCC_Form.CheckBox1.Checked)
					{
						if (decimal.Compare(MyProject.Forms.TCC_Form.WOTLockRPM.Value, 1000m) == 0)
						{
							MyProject.Forms.TCC_Form.WOTLockRPM.Value = new decimal(Conversion.Int((double)RPM.R_Data(1, Convert.ToByte(num46)) * 0.8 / 50.0) * 50.0);
						}
						if (decimal.Compare(num46, WotLck.Value) > 0 && Lock.R_Data((byte)num48, Convert.ToByte(num46)) - U_Shift.R_Data((byte)U_Shift.Grid_X, Convert.ToByte(decimal.Subtract(num46, 1m))) < 15f)
						{
							MyProject.Forms.TCC_Form.WOTStayLocked.Checked = true;
						}
					}
					Lock.W_Data((byte)num48, Convert.ToByte(num46), Speed.R_Data(1, Convert.ToByte(num46)) * (Convert.ToSingle(MyProject.Forms.TCC_Form.WOTLockRPM.Value) / RPM.R_Data(1, Convert.ToByte(num46))) - num2 * Convert.ToSingle(MyProject.Forms.Lead_Form.TCC_Delay.Value));
					if ((decimal.Compare(num46, WotLck.Value) > 0) & MyProject.Forms.TCC_Form.WOTStayLocked.Checked)
					{
						Lock.W_Data((byte)num48, Convert.ToByte(num46), U_Shift.R_Data((byte)U_Shift.Grid_X, Convert.ToByte(decimal.Subtract(num46, 1m))) - 1f);
					}
					Unlock.W_Data((byte)num48, Convert.ToByte(num46), (float)((double)Lock.R_Data((byte)num48, Convert.ToByte(num46)) * 0.95 - 1.0));
				}
				num46 = decimal.Add(num46, 1m);
			}
			int grid_Y15 = Lock.Grid_Y;
			for (int num49 = 1; num49 <= grid_Y15; num49++)
			{
				for (int num50 = Lock.Grid_X; num50 >= 2; num50 += -1)
				{
					if (Lock.R_Data((byte)(num50 - 1), (byte)num49) > Lock.R_Data((byte)num50, (byte)num49))
					{
						Lock.W_Data((byte)(num50 - 1), (byte)num49, Lock.R_Data((byte)num50, (byte)num49));
					}
				}
			}
			int grid_Y16 = Unlock.Grid_Y;
			for (int num51 = 1; num51 <= grid_Y16; num51++)
			{
				for (int num52 = Unlock.Grid_X; num52 >= 2; num52 += -1)
				{
					if (Unlock.R_Data((byte)(num52 - 1), (byte)num51) > Unlock.R_Data((byte)num52, (byte)num51))
					{
						Unlock.W_Data((byte)(num52 - 1), (byte)num51, Unlock.R_Data((byte)num52, (byte)num51));
					}
				}
			}
			int grid_Y17 = Lock.Grid_Y;
			for (int num53 = 1; num53 <= grid_Y17; num53++)
			{
				int num54 = Lock.Grid_X - 3;
				for (int num55 = 1; num55 <= num54; num55++)
				{
					if (decimal.Compare(new decimal(num53), MinLck.Value) < 0)
					{
						Lock.W_Data((byte)num55, (byte)num53, Conversions.ToSingle(Dis_High));
						Unlock.W_Data((byte)num55, (byte)num53, Conversions.ToSingle(Dis_Low));
					}
				}
			}
			int grid_Y18 = Lock.Grid_Y;
			for (int num56 = 1; num56 <= grid_Y18; num56++)
			{
				int num57 = Lock.Grid_X - 2;
				int grid_X14 = Lock.Grid_X;
				for (int num58 = num57; num58 <= grid_X14; num58++)
				{
					if (decimal.Compare(new decimal(num56), WotLck.Value) < 0)
					{
						Lock.W_Data((byte)num58, (byte)num56, Conversions.ToSingle(Dis_High));
						Unlock.W_Data((byte)num58, (byte)num56, Conversions.ToSingle(Dis_Low));
					}
				}
			}
			if ((WOTTCCPrep.Checked & (decimal.Compare(WotLck.Value, new decimal(U_Shift.Grid_Y + 1)) <= 0) & (decimal.Compare(WotLck.Value, 1m) > 0)) && ComboBox1.SelectedIndex >= 3)
			{
				double a = Convert.ToDouble(decimal.Subtract(WotLck.Value, 1m));
				Lock.W_Data((byte)Lock.Grid_X, (byte)Math.Round(a), U_Shift.R_Data((byte)U_Shift.Grid_X, (byte)Math.Round(a)) + 2f);
				Lock.W_Data((byte)(Lock.Grid_X - 1), (byte)Math.Round(a), U_Shift.R_Data((byte)U_Shift.Grid_X, (byte)Math.Round(a)) + 2f);
				Lock.W_Data((byte)(Lock.Grid_X - 2), (byte)Math.Round(a), U_Shift.R_Data((byte)U_Shift.Grid_X, (byte)Math.Round(a)) + 2f);
				Unlock.W_Data((byte)Unlock.Grid_X, (byte)Math.Round(a), U_Shift.R_Data((byte)U_Shift.Grid_X, (byte)Math.Round(a)) + 1f);
				Unlock.W_Data((byte)(Unlock.Grid_X - 1), (byte)Math.Round(a), U_Shift.R_Data((byte)U_Shift.Grid_X, (byte)Math.Round(a)) + 1f);
				Unlock.W_Data((byte)(Unlock.Grid_X - 2), (byte)Math.Round(a), U_Shift.R_Data((byte)U_Shift.Grid_X, (byte)Math.Round(a)) + 1f);
			}
			if (!Allow4L60WOT4th.Checked && ComboBox1.SelectedIndex == 1)
			{
				U_Shift.W_Data((byte)U_Shift.Grid_X, 3, Conversions.ToSingle(Dis_High));
				U_Shift.W_Data((byte)(U_Shift.Grid_X - 1), 3, Conversions.ToSingle(Dis_High));
				U_Shift.W_Data((byte)(U_Shift.Grid_X - 2), 3, Conversions.ToSingle(Dis_High));
				U_Shift.W_Data((byte)(U_Shift.Grid_X - 3), 3, Conversions.ToSingle(Dis_High));
				U_Shift.W_Data((byte)(U_Shift.Grid_X - 4), 3, Conversions.ToSingle(Dis_High));
			}
			if (No2CT_6L.Checked && ComboBox1.SelectedIndex >= 3)
			{
				D_Shift.W_Data(1, 2, D_Shift.R_Data(1, 1));
				D_Shift.W_Data(2, 2, D_Shift.R_Data(2, 1));
				D_Shift.W_Data(3, 2, D_Shift.R_Data(3, 1));
			}
			if (DynoMode.Checked)
			{
				int grid_Y19 = D_Shift.Grid_Y;
				for (int num59 = 1; num59 <= grid_Y19; num59++)
				{
					int grid_X15 = D_Shift.Grid_X;
					for (int num60 = 2; num60 <= grid_X15; num60++)
					{
						D_Shift.W_Data((byte)num60, (byte)num59, D_Shift.R_Data(1, (byte)num59));
					}
				}
				int grid_Y20 = Lock.Grid_Y;
				for (int num61 = 1; num61 <= grid_Y20; num61++)
				{
					int grid_X16 = Lock.Grid_X;
					for (int num62 = 2; num62 <= grid_X16; num62++)
					{
						Lock.W_Data((byte)num62, (byte)num61, Lock.R_Data(1, (byte)num61));
					}
				}
				int grid_Y21 = Unlock.Grid_Y;
				for (int num63 = 1; num63 <= grid_Y21; num63++)
				{
					int grid_X17 = Unlock.Grid_X;
					for (int num64 = 2; num64 <= grid_X17; num64++)
					{
						Unlock.W_Data((byte)num64, (byte)num63, Unlock.R_Data(1, (byte)num63));
					}
				}
			}
			if (RRM.Checked)
			{
				int grid_Y22 = U_Shift.Grid_Y;
				for (int num65 = 1; num65 <= grid_Y22; num65++)
				{
					int num66 = U_Shift.Grid_X - 1;
					for (int num67 = 1; num67 <= num66; num67++)
					{
						U_Shift.W_Data((byte)num67, (byte)num65, U_Shift.R_Data((byte)U_Shift.Grid_X, (byte)num65));
					}
				}
				int grid_Y23 = D_Shift.Grid_Y;
				for (int num68 = 1; num68 <= grid_Y23; num68++)
				{
					int num69 = D_Shift.Grid_X - 1;
					for (int num70 = 1; num70 <= num69; num70++)
					{
						D_Shift.W_Data((byte)num70, (byte)num68, D_Shift.R_Data((byte)D_Shift.Grid_X, (byte)num68));
					}
				}
				int grid_Y24 = Lock.Grid_Y;
				for (int num71 = 1; num71 <= grid_Y24; num71++)
				{
					int grid_X18 = Lock.Grid_X;
					for (int num72 = 2; num72 <= grid_X18; num72++)
					{
						Lock.W_Data((byte)num72, (byte)num71, Lock.R_Data(1, (byte)num71));
					}
				}
				int grid_Y25 = Unlock.Grid_Y;
				for (int num73 = 1; num73 <= grid_Y25; num73++)
				{
					int grid_X19 = Unlock.Grid_X;
					for (int num74 = 2; num74 <= grid_X19; num74++)
					{
						Unlock.W_Data((byte)num74, (byte)num73, Unlock.R_Data(1, (byte)num73));
					}
				}
			}
			if (SGS.Checked)
			{
				int grid_X20 = U_Shift.Grid_X;
				for (int num75 = 1; num75 <= grid_X20; num75++)
				{
					U_Shift.W_Data((byte)num75, 1, 0f);
				}
				int grid_X21 = D_Shift.Grid_X;
				for (int num76 = 1; num76 <= grid_X21; num76++)
				{
					D_Shift.W_Data((byte)num76, 1, 0f);
				}
			}
			GroupBox1.Text = "Shift / Lockup Data";
			if (!Metric.Checked)
			{
				GroupBox1.Text += " (MPH)";
				Speed.Grid_DataScalar = 1f;
				U_Shift.Grid_DataScalar = 1f;
				D_Shift.Grid_DataScalar = 1f;
				Lock.Grid_DataScalar = 1f;
				Unlock.Grid_DataScalar = 1f;
				MyProject.Forms.Export_Form.Export_Grid.Grid_DataScalar = 1f;
			}
			else
			{
				GroupBox1.Text += " (KPH)";
				Speed.Grid_DataScalar = 1.609f;
				U_Shift.Grid_DataScalar = 1.609f;
				D_Shift.Grid_DataScalar = 1.609f;
				Lock.Grid_DataScalar = 1.609f;
				Unlock.Grid_DataScalar = 1.609f;
				MyProject.Forms.Export_Form.Export_Grid.Grid_DataScalar = 1.609f;
			}
			if (num > 0)
			{
				GroupBox1.Text = GroupBox1.Text + "- Data in Logic Error!!! " + Strings.Format((object)num, "0000000");
			}
			if (num == 0)
			{
				U_Shift.Clear_Selected();
				D_Shift.Clear_Selected();
				Lock.Clear_Selected();
				Unlock.Clear_Selected();
			}
			int grid_Y26 = U_Shift.Grid_Y;
			for (int num77 = 1; num77 <= grid_Y26; num77++)
			{
				int grid_X22 = U_Shift.Grid_X;
				for (int num78 = 1; num78 <= grid_X22; num78++)
				{
					if (U_Shift.R_Data((byte)num78, (byte)num77) < 0f)
					{
						U_Shift.W_Data((byte)num78, (byte)num77, 0f);
					}
				}
			}
			int grid_Y27 = D_Shift.Grid_Y;
			for (int num79 = 1; num79 <= grid_Y27; num79++)
			{
				int grid_X23 = D_Shift.Grid_X;
				for (int num80 = 1; num80 <= grid_X23; num80++)
				{
					if (D_Shift.R_Data((byte)num80, (byte)num79) < 0f)
					{
						D_Shift.W_Data((byte)num80, (byte)num79, 0f);
					}
				}
			}
			int grid_Y28 = Lock.Grid_Y;
			for (int num81 = 1; num81 <= grid_Y28; num81++)
			{
				int grid_X24 = Lock.Grid_X;
				for (int num82 = 1; num82 <= grid_X24; num82++)
				{
					if (Lock.R_Data((byte)num82, (byte)num81) < 0f)
					{
						Lock.W_Data((byte)num82, (byte)num81, 0f);
					}
				}
			}
			int grid_Y29 = Unlock.Grid_Y;
			for (int num83 = 1; num83 <= grid_Y29; num83++)
			{
				int grid_X25 = Unlock.Grid_X;
				for (int num84 = 1; num84 <= grid_X25; num84++)
				{
					if (Unlock.R_Data((byte)num84, (byte)num83) < 0f)
					{
						Unlock.W_Data((byte)num84, (byte)num83, 0f);
					}
				}
			}
			MyProject.Forms.Export_Form.Update_VSS();
			MyProject.Forms.Export_Form.Update_Export();
		}
	}

	public void Timer1_Tick(object sender, EventArgs e)
	{
		if ((Init == 0) & (MyProject.Forms.Lead_Form.Init == 0) & (MyProject.Forms.TCC_Form.Init == 0))
		{
			return;
		}
		checked
		{
			if ((Init == 1) & (MyProject.Forms.Lead_Form.Init == 1) & (MyProject.Forms.TCC_Form.Init == 1))
			{
				Setup_Form();
				Setup_Tables();
				Update_Slope();
				MinLck.Value = 3m;
				AclLck.Maximum = 4m;
				AclLck.Value = 4m;
				WotLck.Value = 5m;
				int grid_X = MyProject.Forms.TCC_Form.MinTCC.Grid_X;
				for (int i = 1; i <= grid_X; i++)
				{
					MyProject.Forms.TCC_Form.MinTCC.W_Data((byte)i, 1, 1250f);
					MyProject.Forms.TCC_Form.MinTCC.W_Data((byte)i, 2, 1f);
				}
				MyProject.Forms.TCC_Form.CheckBox1.Checked = true;
				Init = 2;
				MyProject.Forms.Lead_Form.Init = 2;
				MyProject.Forms.TCC_Form.Init = 2;
				if (ComboBox1.Items.Count > 1)
				{
					ComboBox1.SelectedIndex = 1;
				}
				else
				{
					Apply_Default_Config();
				}
			}
			if ((Init == 2) & (MyProject.Forms.Lead_Form.Init == 2) & (MyProject.Forms.TCC_Form.Init == 2))
			{
				ulong num = (ulong)(Ratio.Grid_DataStatus + RPM.Grid_DataStatus + MyProject.Forms.Lead_Form.Delay.Grid_DataStatus + MyProject.Forms.TCC_Form.MinTCC.Grid_DataStatus + MyProject.Forms.OverRide_Form.OverRide_Grid.Grid_DataStatus);
				if (num != PDC)
				{
					US++;
					PDC = num;
				}
				if (OverRide_Enable.Checked)
				{
					OverRide_Capture();
				}
				if (US > 0)
				{
					US = 0;
					Calc_Shifts();
				}
			}
		}
	}

	private void Metric_Click(object sender, EventArgs e)
	{
		float num = 25.4f;
		float num2 = 0.746f;
		float num3 = 0.454f;
		if (Metric.Checked)
		{
			float num4 = Convert.ToSingle(TireVisible.Value);
			float num5 = Convert.ToSingle(MyProject.Forms.Export_Form.NDTire.Value);
			TireVisible.DecimalPlaces = 0;
			TireVisible.Increment = 1m;
			TireVisible.Maximum = new decimal(150f * num);
			TireVisible.Minimum = new decimal(5f * num);
			MyProject.Forms.Export_Form.NDTire.DecimalPlaces = 0;
			MyProject.Forms.Export_Form.NDTire.Increment = 1m;
			MyProject.Forms.Export_Form.NDTire.Maximum = new decimal(150f * num);
			MyProject.Forms.Export_Form.NDTire.Minimum = new decimal(5f * num);
			TireVisible.Value = new decimal(num4 * num);
			MyProject.Forms.Export_Form.NDTire.Value = new decimal(num5 * num);
			num4 = Convert.ToSingle(MyProject.Forms.Lead_Form.WeightVisible.Value);
			MyProject.Forms.Lead_Form.WeightVisible.Maximum = new decimal(25000f * num3);
			MyProject.Forms.Lead_Form.WeightVisible.Minimum = new decimal(250f * num3);
			MyProject.Forms.Lead_Form.WeightVisible.Value = new decimal(num4 * num3);
			num4 = Convert.ToSingle(MyProject.Forms.Lead_Form.RWHPVisible.Value);
			MyProject.Forms.Lead_Form.RWHPVisible.Increment = 1m;
			MyProject.Forms.Lead_Form.RWHPVisible.Maximum = new decimal(2000f * num2);
			MyProject.Forms.Lead_Form.RWHPVisible.Minimum = new decimal(10f * num2);
			MyProject.Forms.Lead_Form.RWHPVisible.Value = new decimal(num4 * num2);
			MyProject.Forms.Tire_Form.Label4.Text = "mm";
		}
		else
		{
			float num4 = Convert.ToSingle(TireVisible.Value);
			float num5 = Convert.ToSingle(MyProject.Forms.Export_Form.NDTire.Value);
			TireVisible.DecimalPlaces = 2;
			TireVisible.Increment = 0.1m;
			TireVisible.Maximum = 150m;
			TireVisible.Minimum = 5m;
			MyProject.Forms.Export_Form.NDTire.DecimalPlaces = 2;
			MyProject.Forms.Export_Form.NDTire.Increment = 0.1m;
			MyProject.Forms.Export_Form.NDTire.Maximum = 150m;
			MyProject.Forms.Export_Form.NDTire.Minimum = 5m;
			TireVisible.Value = new decimal(num4 / num);
			MyProject.Forms.Export_Form.NDTire.Value = new decimal(num5 / num);
			num4 = Convert.ToSingle(MyProject.Forms.Lead_Form.WeightVisible.Value);
			MyProject.Forms.Lead_Form.WeightVisible.Maximum = 25000m;
			MyProject.Forms.Lead_Form.WeightVisible.Minimum = 250m;
			MyProject.Forms.Lead_Form.WeightVisible.Value = new decimal(num4 / num3);
			num4 = Convert.ToSingle(MyProject.Forms.Lead_Form.RWHPVisible.Value);
			MyProject.Forms.Lead_Form.RWHPVisible.Increment = 5m;
			MyProject.Forms.Lead_Form.RWHPVisible.Maximum = 2000m;
			MyProject.Forms.Lead_Form.RWHPVisible.Minimum = 10m;
			MyProject.Forms.Lead_Form.RWHPVisible.Value = new decimal(num4 / num2);
			MyProject.Forms.Tire_Form.Label4.Text = "in";
		}
		MyProject.Forms.Tire_Form.Label5.Text = MyProject.Forms.Tire_Form.Label4.Text;
		MyProject.Forms.Tire_Form.Label7.Text = MyProject.Forms.Tire_Form.Label4.Text;
		MyProject.Forms.Tire_Form.Label10.Text = MyProject.Forms.Tire_Form.Label4.Text;
		MyProject.Forms.Tire_Form.Button1_Click(null, null);
		checked
		{
			US++;
		}
	}

	private void DynoMode_Click(object sender, EventArgs e)
	{
		checked
		{
			US++;
		}
	}

	private void RRM_Click(object sender, EventArgs e)
	{
		checked
		{
			US++;
		}
	}

	private void SGS_Click(object sender, EventArgs e)
	{
		checked
		{
			US++;
		}
	}

	private void Allow4L60WOT4th_Click(object sender, EventArgs e)
	{
		checked
		{
			US++;
		}
	}

	private void WOTTCCPrep_Click(object sender, EventArgs e)
	{
		checked
		{
			US++;
		}
	}

	private void No2CT_6L_Click(object sender, EventArgs e)
	{
		checked
		{
			US++;
		}
	}

	private void StallLogic_Click(object sender, EventArgs e)
	{
		checked
		{
			US++;
		}
	}

	private void MaxSpeed_Locked_Click(object sender, EventArgs e)
	{
		checked
		{
			US++;
		}
	}

	private void LeadRpm_Click(object sender, EventArgs e)
	{
		checked
		{
			US++;
		}
	}

	private void ULckStay_Click(object sender, EventArgs e)
	{
		checked
		{
			US++;
		}
	}

	private void InitLock_Click(object sender, EventArgs e)
	{
		checked
		{
			US++;
		}
	}

	private void PreLock_Click(object sender, EventArgs e)
	{
		checked
		{
			US++;
		}
	}

	private void PostLock_Click(object sender, EventArgs e)
	{
		checked
		{
			US++;
		}
	}

	private void LockUnlock_Click(object sender, EventArgs e)
	{
		checked
		{
			US++;
		}
	}

	private void UpDown_Click(object sender, EventArgs e)
	{
		checked
		{
			US++;
		}
	}

	private void ShiftMax_Click(object sender, EventArgs e)
	{
		checked
		{
			US++;
		}
	}

	private void Shift_Spread_Click(object sender, EventArgs e)
	{
		checked
		{
			if (Init >= 1)
			{
				float num = 0f;
				num = (float)Conversion.Val(((ToolStripControlHost)Shift_Spread).Text);
				if (num < 1f)
				{
					num = 1f;
				}
				if (num > 10f)
				{
					num = 10f;
				}
				((ToolStripControlHost)Shift_Spread).Text = Conversion.Str((object)num);
				US++;
			}
		}
	}

	private void Lock_Spread_Click(object sender, EventArgs e)
	{
		checked
		{
			if (Init >= 1)
			{
				float num = 0f;
				num = (float)Conversion.Val(((ToolStripControlHost)Lock_Spread).Text);
				if (num < 1f)
				{
					num = 1f;
				}
				if (num > 10f)
				{
					num = 10f;
				}
				((ToolStripControlHost)Lock_Spread).Text = Conversion.Str((object)num);
				US++;
			}
		}
	}

	private void Lock_UpShift_Spread_Click(object sender, EventArgs e)
	{
		checked
		{
			if (Init >= 1)
			{
				float num = 0f;
				num = (float)Conversion.Val(((ToolStripControlHost)Lock_Shift_Spread).Text);
				if (num < 1f)
				{
					num = 1f;
				}
				if (num > 10f)
				{
					num = 10f;
				}
				((ToolStripControlHost)Lock_Shift_Spread).Text = Conversion.Str((object)num);
				US++;
			}
		}
	}

	private void Unlock_Downshift_Spread_Click(object sender, EventArgs e)
	{
		checked
		{
			if (Init >= 1)
			{
				float num = 0f;
				num = (float)Conversion.Val(((ToolStripControlHost)Unlock_Shift_Spread).Text);
				if (num < 1f)
				{
					num = 1f;
				}
				if (num > 10f)
				{
					num = 10f;
				}
				((ToolStripControlHost)Unlock_Shift_Spread).Text = Conversion.Str((object)num);
				US++;
			}
		}
	}

	private void OpenToolStripMenuItem_Click(object sender, EventArgs e)
	{
		//IL_0010: Unknown result type (might be due to invalid IL or missing references)
		//IL_0016: Invalid comparison between Unknown and I4
		if (Init >= 1 && (int)((CommonDialog)OpenFileDialog1).ShowDialog() == 1)
		{
			((FileDialog)SaveFileDialog1).FileName = ((FileDialog)OpenFileDialog1).FileName;
			Read_Trans(((FileDialog)OpenFileDialog1).FileName);
		}
	}

	private void SaveToolStripMenuItem_Click(object sender, EventArgs e)
	{
		//IL_0010: Unknown result type (might be due to invalid IL or missing references)
		//IL_0016: Invalid comparison between Unknown and I4
		if (Init >= 1 && (int)((CommonDialog)SaveFileDialog1).ShowDialog() == 1)
		{
			((FileDialog)OpenFileDialog1).FileName = ((FileDialog)SaveFileDialog1).FileName;
			Write_Trans(((FileDialog)SaveFileDialog1).FileName);
		}
	}

	private void ExportWindowToolStripMenuItem_Click(object sender, EventArgs e)
	{
		if (Init >= 1)
		{
			((Control)MyProject.Forms.Export_Form).Show();
			((Form)MyProject.Forms.Export_Form).WindowState = (FormWindowState)0;
			((Control)MyProject.Forms.Export_Form).Focus();
		}
	}

	private void AboutToolStripMenuItem_Click(object sender, EventArgs e)
	{
		//IL_000c: Unknown result type (might be due to invalid IL or missing references)
		MessageBox.Show("Bluecat Transmission Calibration Generator V1.42.431\r\nFree to use. If it saved you time, hassle, or money, a tip is always greatly appreciated:\r\n\r\nPayPal:  tunedbybluecat@gmail.com", "About", (MessageBoxButtons)0, (MessageBoxIcon)0);
	}

	public void Write_Trans(string FN)
	{
		StreamWriter TempFile = new StreamWriter(FN);
		string text = Strings.Format((object)Gears.Value, "");
		PutFileData(ref TempFile, "Gears\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = Strings.Format((object)VSS.Value, "");
		PutFileData(ref TempFile, "VSS\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = Strings.Format((object)MyProject.Forms.Lead_Form.Lead.Value, "");
		PutFileData(ref TempFile, "Lead\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		decimal value = Gears.Value;
		decimal num = 1m;
		while (ForLoopControl.ForNextCheckDec(num, value, 1m))
		{
			text = Strings.Format((object)Ratio.R_Data(1, Convert.ToByte(num)), "");
			PutFileData(ref TempFile, "Ratio" + Strings.Format((object)num, "") + "\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			num = decimal.Add(num, 1m);
		}
		text = Strings.Format((object)ComboBox1.SelectedIndex, "");
		PutFileData(ref TempFile, "Trans\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		decimal value2 = Gears.Value;
		decimal num2 = 1m;
		while (ForLoopControl.ForNextCheckDec(num2, value2, 1m))
		{
			text = Strings.Format((object)RPM.R_Data(1, Convert.ToByte(num2)), "");
			PutFileData(ref TempFile, "RPM" + Strings.Format((object)num2, "") + "\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			num2 = decimal.Add(num2, 1m);
		}
		text = Strings.Format((object)Gear.Value, "");
		PutFileData(ref TempFile, "Gear\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = Strings.Format((object)Tire.Value, "");
		PutFileData(ref TempFile, "Tire\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = Strings.Format((object)Idle.Value, "");
		PutFileData(ref TempFile, "Idle\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = Strings.Format((object)DRPM.Value, "");
		PutFileData(ref TempFile, "DownRPM\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = Strings.Format((object)Stall.Value, "");
		PutFileData(ref TempFile, "Stall\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = Strings.Format((object)MyProject.Forms.TCC_Form.MinTCC.R_Data(1, 1), "");
		PutFileData(ref TempFile, "MinLockRPM\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = Strings.Format((object)MinLck.Value, "");
		PutFileData(ref TempFile, "MinLockGear\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = Strings.Format((object)AclLck.Value, "");
		PutFileData(ref TempFile, "AccelLockGear\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = Strings.Format((object)WotLck.Value, "");
		PutFileData(ref TempFile, "WOTLockGear\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = Strings.Format((object)Factor.Value, "");
		PutFileData(ref TempFile, "Factor\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = Strings.Format((object)Offset.Value, "");
		PutFileData(ref TempFile, "Offset\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = Strings.Format((object)UpF.Value, "");
		PutFileData(ref TempFile, "UpFactor\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = Strings.Format((object)DownF.Value, "");
		PutFileData(ref TempFile, "DownFactor\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = Strings.Format((object)ComboBox2.SelectedIndex, "");
		PutFileData(ref TempFile, "TBSlope\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = ((!Metric.Checked) ? "0" : "1");
		PutFileData(ref TempFile, "Metric\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = ((!Allow4L60WOT4th.Checked) ? "0" : "1");
		PutFileData(ref TempFile, "Allow4L60WOT4th\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = ((!StallLogic.Checked) ? "0" : "1");
		PutFileData(ref TempFile, "StallLogic\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = ((MyProject.Forms.TCC_Form.MinTCC.R_Data(1, 2) == 0f) ? "0" : "1");
		PutFileData(ref TempFile, "UnlockonDownShift\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = ((!InitLock.Checked) ? "0" : "1");
		PutFileData(ref TempFile, "AccelGearLock\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = ((!PreLock.Checked) ? "0" : "1");
		PutFileData(ref TempFile, "PreAccelGearLock\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = ((!PostLock.Checked) ? "0" : "1");
		PutFileData(ref TempFile, "PostAccelGearLock\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = ((!LockUnlock.Checked) ? "0" : "1");
		PutFileData(ref TempFile, "Lock>Unlock\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = ((!UpDown.Checked) ? "0" : "1");
		PutFileData(ref TempFile, "Up>Down\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = ((!ShiftMax.Checked) ? "0" : "1");
		PutFileData(ref TempFile, "Shift<Max\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = ((ToolStripControlHost)Shift_Spread).Text;
		PutFileData(ref TempFile, "ShiftSpread\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = ((ToolStripControlHost)Lock_Spread).Text;
		PutFileData(ref TempFile, "LockSpread\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = ((ToolStripControlHost)Lock_Shift_Spread).Text;
		PutFileData(ref TempFile, "ShiftLockSpread\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = ((ToolStripControlHost)Unlock_Shift_Spread).Text;
		PutFileData(ref TempFile, "UnlockShiftSpread\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = ((!MyProject.Forms.TCC_Form.CheckBox1.Checked) ? "0" : "1");
		PutFileData(ref TempFile, "AUTOWOT\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = Strings.Format((object)MyProject.Forms.TCC_Form.WOTLockRPM.Value, "");
		PutFileData(ref TempFile, "WOTLockRPM\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = ((!MyProject.Forms.TCC_Form.WOTStayLocked.Checked) ? "0" : "1");
		PutFileData(ref TempFile, "WOTStayLocked\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = ((!DynoMode.Checked) ? "0" : "1");
		PutFileData(ref TempFile, "DynoMode\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = ((!LeadRpm.Checked) ? "0" : "1");
		PutFileData(ref TempFile, "LeadShiftRPM\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = Strings.Format((object)MyProject.Forms.Export_Form.ComboBox2.SelectedIndex, "");
		PutFileData(ref TempFile, "VSSMode\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = Strings.Format((object)MyProject.Forms.Export_Form.ComboBox1.SelectedIndex, "");
		PutFileData(ref TempFile, "ExportMode\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = ((!MyProject.Forms.Export_Form.CheckBox1.Checked) ? "0" : "1");
		PutFileData(ref TempFile, "2C_WOT\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = ((!MaxSpeed_Locked.Checked) ? "0" : "1");
		PutFileData(ref TempFile, "UseLockedSpeed\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = ((!No2CT_6L.Checked) ? "0" : "1");
		PutFileData(ref TempFile, "No6L_CT2nd\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = ((!ULckStay.Checked) ? "0" : "1");
		PutFileData(ref TempFile, "UnlockStay\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = (MyProject.Forms.Lead_Form.Lead_Radio1.Checked ? "0" : "1");
		PutFileData(ref TempFile, "AdvancedLead\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = Strings.Format((object)MyProject.Forms.Lead_Form.Weight.Value, "");
		PutFileData(ref TempFile, "Weight\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = Strings.Format((object)MyProject.Forms.Lead_Form.RWHP.Value, "");
		PutFileData(ref TempFile, "RWHP\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = Strings.Format((object)MyProject.Forms.Lead_Form.TCC_Delay.Value, "");
		PutFileData(ref TempFile, "TCC_Delay\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		text = Strings.Format((object)MyProject.Forms.Lead_Form.Down_Time.Value, "");
		PutFileData(ref TempFile, "DownTime\r\n");
		PutFileData(ref TempFile, text + "\r\n");
		decimal num3 = decimal.Subtract(Gears.Value, 1m);
		decimal num4 = 1m;
		while (ForLoopControl.ForNextCheckDec(num4, num3, 1m))
		{
			text = Strings.Format((object)MyProject.Forms.Lead_Form.Delay.R_Data(1, Convert.ToByte(num4)), "");
			PutFileData(ref TempFile, "Prep" + Strings.Format((object)num4, "") + "\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			num4 = decimal.Add(num4, 1m);
		}
		decimal num5 = decimal.Subtract(Gears.Value, 1m);
		decimal num6 = 1m;
		while (ForLoopControl.ForNextCheckDec(num6, num5, 1m))
		{
			text = Strings.Format((object)MyProject.Forms.Lead_Form.Delay.R_Data(2, Convert.ToByte(num6)), "");
			PutFileData(ref TempFile, "React" + Strings.Format((object)num6, "") + "\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			num6 = decimal.Add(num6, 1m);
		}
		int num7 = 1;
		checked
		{
			do
			{
				text = Strings.Format((object)MyProject.Forms.TCC_Form.MinTCC.R_Data((byte)num7, 1), "");
				PutFileData(ref TempFile, "MinTCCRPM" + Strings.Format((object)num7, "") + "\r\n");
				PutFileData(ref TempFile, text + "\r\n");
				num7++;
			}
			while (num7 <= 17);
			int num8 = 1;
			do
			{
				text = Strings.Format((object)MyProject.Forms.TCC_Form.MinTCC.R_Data((byte)num8, 2), "");
				PutFileData(ref TempFile, "TCC_UlckBeforeDown" + Strings.Format((object)num8, "") + "\r\n");
				PutFileData(ref TempFile, text + "\r\n");
				num8++;
			}
			while (num8 <= 17);
			decimal value3 = Gears.Value;
			decimal num9 = 2m;
			while (ForLoopControl.ForNextCheckDec(num9, value3, 1m))
			{
				int num10 = 1;
				do
				{
					text = Strings.Format((object)MyProject.Forms.TCC_Form.MinTCC.R_Data((byte)num10, Convert.ToByte(decimal.Subtract(decimal.Multiply(num9, 2m), 1m))), "");
					PutFileData(ref TempFile, "MinTCCRPM" + Strings.Format((object)num10, "") + "-" + Strings.Format((object)num9, "") + "\r\n");
					PutFileData(ref TempFile, text + "\r\n");
					num10++;
				}
				while (num10 <= 17);
				int num11 = 1;
				do
				{
					text = Strings.Format((object)MyProject.Forms.TCC_Form.MinTCC.R_Data((byte)num11, Convert.ToByte(decimal.Multiply(num9, 2m))), "");
					PutFileData(ref TempFile, "TCC_UlckBeforeDown" + Strings.Format((object)num11, "") + "-" + Strings.Format((object)num9, "") + "\r\n");
					PutFileData(ref TempFile, text + "\r\n");
					num11++;
				}
				while (num11 <= 17);
				num9 = decimal.Add(num9, 1m);
			}
			text = Strings.Format((object)MyProject.Forms.TCC_Form.MinTCCrpm.Value, "");
			PutFileData(ref TempFile, "TCC_MinRpm\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			text = Strings.Format((object)MyProject.Forms.TCC_Form.MinTCCmintps.Value, "");
			PutFileData(ref TempFile, "TCC_MinTps\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			text = Strings.Format((object)MyProject.Forms.TCC_Form.MinTCCmaxtps.Value, "");
			PutFileData(ref TempFile, "TCC_MaxTps\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			text = ((!SGS.Checked) ? "0" : "1");
			PutFileData(ref TempFile, "SecondGearStart\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			text = ((!MyProject.Forms.Export_Form.CheckBox2.Checked) ? "0" : "1");
			PutFileData(ref TempFile, "Exp_SpeedoCal\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			text = ((!MyProject.Forms.Export_Form.CheckBox3.Checked) ? "0" : "1");
			PutFileData(ref TempFile, "Exp_IncludeTUTD\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			text = ((!MyProject.Forms.Export_Form.CheckBox4.Checked) ? "0" : "1");
			PutFileData(ref TempFile, "Exp_Normal\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			text = ((!MyProject.Forms.Export_Form.CheckBox5.Checked) ? "0" : "1");
			PutFileData(ref TempFile, "Exp_PatternA\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			text = ((!MyProject.Forms.Export_Form.CheckBox6.Checked) ? "0" : "1");
			PutFileData(ref TempFile, "Exp_PatternB\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			text = ((!MyProject.Forms.Export_Form.CheckBox7.Checked) ? "0" : "1");
			PutFileData(ref TempFile, "Exp_Hot\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			text = ((!MyProject.Forms.Export_Form.CheckBox8.Checked) ? "0" : "1");
			PutFileData(ref TempFile, "Exp_TUTDAutoWOT\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			text = ((!MyProject.Forms.Export_Form.CheckBox9.Checked) ? "0" : "1");
			PutFileData(ref TempFile, "Exp_IncludeSafety\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			text = ((!MyProject.Forms.Export_Form.CheckBox10.Checked) ? "0" : "1");
			PutFileData(ref TempFile, "Exp_IncludeExtra\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			text = ((!MyProject.Forms.Export_Form.CheckBox11.Checked) ? "0" : "1");
			PutFileData(ref TempFile, "Exp_ZeroExtra\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			text = ((!MyProject.Forms.Export_Form.CheckBox12.Checked) ? "0" : "1");
			PutFileData(ref TempFile, "Exp_ZeroSafety\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			text = ((!MyProject.Forms.Export_Form.CheckBox13.Checked) ? "0" : "1");
			PutFileData(ref TempFile, "Exp_LowRange\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			text = ((!MyProject.Forms.Export_Form.CheckBox14.Checked) ? "0" : "1");
			PutFileData(ref TempFile, "Exp_ManualLowerGear\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			text = ((!MyProject.Forms.Export_Form.CheckBox15.Checked) ? "0" : "1");
			PutFileData(ref TempFile, "Exp_UnitBugECM\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			text = ((!MyProject.Forms.Export_Form.CheckBox16.Checked) ? "0" : "1");
			PutFileData(ref TempFile, "Exp_UnitBugTCM\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			text = ((!MyProject.Forms.Export_Form.CheckBox17.Checked) ? "0" : "1");
			PutFileData(ref TempFile, "Exp_DiffFromDriven\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			text = Strings.Format((object)MyProject.Forms.Export_Form.ComboBox3.SelectedIndex, "");
			PutFileData(ref TempFile, "Exp_PatternAPreset\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			text = Strings.Format((object)MyProject.Forms.Export_Form.ComboBox4.SelectedIndex, "");
			PutFileData(ref TempFile, "Exp_PatternBPreset\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			text = Strings.Format((object)MyProject.Forms.Export_Form.Gear.Value, "");
			PutFileData(ref TempFile, "Exp_DrivenRatio\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			text = Strings.Format((object)MyProject.Forms.Export_Form.NDTire.Value, "");
			PutFileData(ref TempFile, "Exp_NDTire\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			text = ((!OverRide_Enable.Checked) ? "0" : "1");
			PutFileData(ref TempFile, "SlopeOverride\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			decimal num12 = decimal.Multiply(decimal.Subtract(Gears.Value, 1m), 2m);
			decimal num13 = 1m;
			while (ForLoopControl.ForNextCheckDec(num13, num12, 1m))
			{
				int num14 = 1;
				do
				{
					text = Strings.Format((object)MyProject.Forms.OverRide_Form.OverRide_Grid.R_Data((byte)num14, Convert.ToByte(num13)), "");
					PutFileData(ref TempFile, "SlopeOverride" + Strings.Format((object)num14, "") + "-" + Strings.Format((object)num13, "") + "\r\n");
					PutFileData(ref TempFile, text + "\r\n");
					num14++;
				}
				while (num14 <= 17);
				num13 = decimal.Add(num13, 1m);
			}
			text = ((!MyProject.Forms.Export_Form.CheckBox18.Checked) ? "0" : "1");
			PutFileData(ref TempFile, "Exp_PatternC\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			text = ((!MyProject.Forms.Export_Form.CheckBox19.Checked) ? "0" : "1");
			PutFileData(ref TempFile, "Exp_TCCMin\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			text = ((!MyProject.Forms.Export_Form.CheckBox20.Checked) ? "0" : "1");
			PutFileData(ref TempFile, "Exp_VSS\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			text = ((!RRM.Checked) ? "0" : "1");
			PutFileData(ref TempFile, "RollRaceMode\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			text = ((!MyProject.Forms.Export_Form.CheckBox21.Checked) ? "0" : "1");
			PutFileData(ref TempFile, "Exp_AlwaysOnTop\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			text = ((!WOTTCCPrep.Checked) ? "0" : "1");
			PutFileData(ref TempFile, "WOTTCCPrep\r\n");
			PutFileData(ref TempFile, text + "\r\n");
			TempFile.Close();
		}
	}

	public void Read_Trans(string FN)
	{
		StreamReader TempFile = new StreamReader(FN);
		OverRide_Enable.Checked = false;
		OverRide_Zero();
		SGS.Checked = false;
		MyProject.Forms.Export_Form.CheckBox2.Checked = true;
		MyProject.Forms.Export_Form.CheckBox3.Checked = true;
		MyProject.Forms.Export_Form.CheckBox4.Checked = true;
		MyProject.Forms.Export_Form.CheckBox5.Checked = true;
		MyProject.Forms.Export_Form.CheckBox6.Checked = true;
		MyProject.Forms.Export_Form.CheckBox7.Checked = true;
		MyProject.Forms.Export_Form.CheckBox8.Checked = false;
		MyProject.Forms.Export_Form.CheckBox9.Checked = true;
		MyProject.Forms.Export_Form.CheckBox10.Checked = true;
		MyProject.Forms.Export_Form.CheckBox11.Checked = false;
		MyProject.Forms.Export_Form.CheckBox12.Checked = false;
		MyProject.Forms.Export_Form.CheckBox13.Checked = false;
		MyProject.Forms.Export_Form.CheckBox14.Checked = false;
		MyProject.Forms.Export_Form.CheckBox15.Checked = false;
		MyProject.Forms.Export_Form.CheckBox16.Checked = false;
		MyProject.Forms.Export_Form.CheckBox17.Checked = false;
		MyProject.Forms.Export_Form.ComboBox3.SelectedIndex = 0;
		MyProject.Forms.Export_Form.ComboBox4.SelectedIndex = 0;
		MyProject.Forms.Export_Form.Gear.Value = 2.72m;
		MyProject.Forms.Export_Form.NDTire.Value = TireVisible.Value;
		MyProject.Forms.Export_Form.CheckBox18.Checked = true;
		MyProject.Forms.Export_Form.CheckBox19.Checked = false;
		MyProject.Forms.Export_Form.CheckBox20.Checked = false;
		RRM.Checked = false;
		MyProject.Forms.Export_Form.CheckBox21.Checked = false;
		WOTTCCPrep.Checked = true;
		string fileData = GetFileData(ref TempFile);
		checked
		{
			if (Strings.Len(fileData) >= 3 && D_SC == 13)
			{
				fileData = GetFileData(ref TempFile);
				if (D_SC == 13)
				{
					float value = (float)Conversion.Val(fileData);
					Gears.Value = new decimal(value);
					fileData = GetFileData(ref TempFile);
					if (Strings.Len(fileData) >= 3 && D_SC == 13)
					{
						fileData = GetFileData(ref TempFile);
						if (D_SC == 13)
						{
							float value2 = (float)Conversion.Val(fileData);
							VSS.Value = new decimal(value2);
							fileData = GetFileData(ref TempFile);
							if (Strings.Len(fileData) >= 3 && D_SC == 13)
							{
								fileData = GetFileData(ref TempFile);
								if (D_SC == 13)
								{
									float value3 = (float)Conversion.Val(fileData);
									MyProject.Forms.Lead_Form.Lead.Value = new decimal(value3);
									decimal value4 = Gears.Value;
									decimal num = 1m;
									while (true)
									{
										if (ForLoopControl.ForNextCheckDec(num, value4, 1m))
										{
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											Ratio.W_Data(1, Convert.ToByte(num), (float)Conversion.Val(fileData));
											num = decimal.Add(num, 1m);
											continue;
										}
										fileData = GetFileData(ref TempFile);
										if (Strings.Len(fileData) < 3 || D_SC != 13)
										{
											break;
										}
										fileData = GetFileData(ref TempFile);
										if (D_SC != 13)
										{
											break;
										}
										ComboBox1.SelectedIndex = (int)Math.Round(Conversion.Val(fileData));
										Gears.Value = new decimal(value);
										VSS.Value = new decimal(value2);
										MyProject.Forms.Lead_Form.Lead.Value = new decimal(value3);
										decimal value5 = Gears.Value;
										decimal num2 = 1m;
										while (true)
										{
											if (ForLoopControl.ForNextCheckDec(num2, value5, 1m))
											{
												fileData = GetFileData(ref TempFile);
												if (Strings.Len(fileData) < 3 || D_SC != 13)
												{
													break;
												}
												fileData = GetFileData(ref TempFile);
												if (D_SC != 13)
												{
													break;
												}
												RPM.W_Data(1, Convert.ToByte(num2), (float)Conversion.Val(fileData));
												num2 = decimal.Add(num2, 1m);
												continue;
											}
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											Gear.Value = new decimal(Conversion.Val(fileData));
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											Tire.Value = new decimal(Conversion.Val(fileData));
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											Idle.Value = new decimal(Conversion.Val(fileData));
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											DRPM.Value = new decimal(Conversion.Val(fileData));
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											Stall.Value = new decimal(Conversion.Val(fileData));
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											decimal value6 = Gears.Value;
											decimal num3 = 1m;
											while (ForLoopControl.ForNextCheckDec(num3, value6, 1m))
											{
												int num4 = 1;
												do
												{
													MyProject.Forms.TCC_Form.MinTCC.W_Data((byte)num4, Convert.ToByte(decimal.Subtract(decimal.Multiply(num3, 2m), 1m)), (float)Conversion.Val(fileData));
													num4++;
												}
												while (num4 <= 17);
												num3 = decimal.Add(num3, 1m);
											}
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											MinLck.Value = new decimal(Conversion.Val(fileData));
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											AclLck.Value = new decimal(Conversion.Val(fileData));
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											WotLck.Value = new decimal(Conversion.Val(fileData));
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											Factor.Value = new decimal(Conversion.Val(fileData));
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											Offset.Value = new decimal(Conversion.Val(fileData));
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											UpF.Value = new decimal(Conversion.Val(fileData));
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											DownF.Value = new decimal(Conversion.Val(fileData));
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											ComboBox2.SelectedIndex = (int)Math.Round(Conversion.Val(fileData));
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											if (Operators.CompareString(fileData, "1", false) == 0)
											{
												Metric.Checked = true;
											}
											else
											{
												Metric.Checked = false;
											}
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											if (Operators.CompareString(fileData, "1", false) == 0)
											{
												Allow4L60WOT4th.Checked = true;
											}
											else
											{
												Allow4L60WOT4th.Checked = false;
											}
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											if (Operators.CompareString(fileData, "1", false) == 0)
											{
												StallLogic.Checked = true;
											}
											else
											{
												StallLogic.Checked = false;
											}
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											if (Operators.CompareString(fileData, "0", false) != 0)
											{
												fileData = "1";
											}
											decimal value7 = Gears.Value;
											decimal num5 = 1m;
											while (ForLoopControl.ForNextCheckDec(num5, value7, 1m))
											{
												int num6 = 1;
												do
												{
													MyProject.Forms.TCC_Form.MinTCC.W_Data((byte)num6, Convert.ToByte(decimal.Multiply(num5, 2m)), (float)Conversion.Val(fileData));
													num6++;
												}
												while (num6 <= 17);
												num5 = decimal.Add(num5, 1m);
											}
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											if (Operators.CompareString(fileData, "1", false) == 0)
											{
												InitLock.Checked = true;
											}
											else
											{
												InitLock.Checked = false;
											}
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											if (Operators.CompareString(fileData, "1", false) == 0)
											{
												PreLock.Checked = true;
											}
											else
											{
												PreLock.Checked = false;
											}
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											if (Operators.CompareString(fileData, "1", false) == 0)
											{
												PostLock.Checked = true;
											}
											else
											{
												PostLock.Checked = false;
											}
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											if (Operators.CompareString(fileData, "1", false) == 0)
											{
												LockUnlock.Checked = true;
											}
											else
											{
												LockUnlock.Checked = false;
											}
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											if (Operators.CompareString(fileData, "1", false) == 0)
											{
												UpDown.Checked = true;
											}
											else
											{
												UpDown.Checked = false;
											}
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											if (Operators.CompareString(fileData, "1", false) == 0)
											{
												ShiftMax.Checked = true;
											}
											else
											{
												ShiftMax.Checked = false;
											}
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											((ToolStripControlHost)Shift_Spread).Text = fileData;
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											((ToolStripControlHost)Lock_Spread).Text = fileData;
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											((ToolStripControlHost)Lock_Shift_Spread).Text = fileData;
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											((ToolStripControlHost)Unlock_Shift_Spread).Text = fileData;
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											if (Operators.CompareString(fileData, "1", false) == 0)
											{
												MyProject.Forms.TCC_Form.CheckBox1.Checked = true;
											}
											else
											{
												MyProject.Forms.TCC_Form.CheckBox1.Checked = false;
											}
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											MyProject.Forms.TCC_Form.WOTLockRPM.Value = new decimal(Conversion.Val(fileData));
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											if (Operators.CompareString(fileData, "1", false) == 0)
											{
												MyProject.Forms.TCC_Form.WOTStayLocked.Checked = true;
											}
											else
											{
												MyProject.Forms.TCC_Form.WOTStayLocked.Checked = false;
											}
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											if (Operators.CompareString(fileData, "1", false) == 0)
											{
												DynoMode.Checked = true;
											}
											else
											{
												DynoMode.Checked = false;
											}
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											if (Operators.CompareString(fileData, "1", false) == 0)
											{
												LeadRpm.Checked = true;
											}
											else
											{
												LeadRpm.Checked = false;
											}
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											MyProject.Forms.Export_Form.ComboBox2.SelectedIndex = (int)Math.Round(Conversion.Val(fileData));
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											MyProject.Forms.Export_Form.ComboBox1.SelectedIndex = (int)Math.Round(Conversion.Val(fileData));
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											if (Operators.CompareString(fileData, "1", false) == 0)
											{
												MyProject.Forms.Export_Form.CheckBox1.Checked = true;
											}
											else
											{
												MyProject.Forms.Export_Form.CheckBox1.Checked = false;
											}
											MyProject.Forms.Lead_Form.Lead_Radio1.Checked = true;
											MaxSpeed_Locked.Checked = false;
											ULckStay.Checked = false;
											No2CT_6L.Checked = false;
											MyProject.Forms.Lead_Form.Weight.Value = 3600m;
											MyProject.Forms.Lead_Form.RWHP.Value = 300m;
											MyProject.Forms.Lead_Form.TCC_Delay.Value = 0.5m;
											MyProject.Forms.Lead_Form.Down_Time.Value = 0.5m;
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											if (Operators.CompareString(fileData, "1", false) == 0)
											{
												MaxSpeed_Locked.Checked = true;
											}
											else
											{
												MaxSpeed_Locked.Checked = false;
											}
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											if (Operators.CompareString(fileData, "1", false) == 0)
											{
												No2CT_6L.Checked = true;
											}
											else
											{
												No2CT_6L.Checked = false;
											}
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											if (Operators.CompareString(fileData, "1", false) == 0)
											{
												ULckStay.Checked = true;
											}
											else
											{
												ULckStay.Checked = false;
											}
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											if (Operators.CompareString(fileData, "1", false) == 0)
											{
												MyProject.Forms.Lead_Form.Lead_Radio2.Checked = true;
											}
											else
											{
												MyProject.Forms.Lead_Form.Lead_Radio1.Checked = true;
											}
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											MyProject.Forms.Lead_Form.Weight.Value = new decimal(Conversion.Val(fileData));
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											MyProject.Forms.Lead_Form.RWHP.Value = new decimal(Conversion.Val(fileData));
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											MyProject.Forms.Lead_Form.TCC_Delay.Value = new decimal(Conversion.Val(fileData));
											fileData = GetFileData(ref TempFile);
											if (Strings.Len(fileData) < 3 || D_SC != 13)
											{
												break;
											}
											fileData = GetFileData(ref TempFile);
											if (D_SC != 13)
											{
												break;
											}
											MyProject.Forms.Lead_Form.Down_Time.Value = new decimal(Conversion.Val(fileData));
											decimal num7 = decimal.Subtract(Gears.Value, 1m);
											decimal num8 = 1m;
											while (true)
											{
												if (ForLoopControl.ForNextCheckDec(num8, num7, 1m))
												{
													fileData = GetFileData(ref TempFile);
													if (Strings.Len(fileData) < 3 || D_SC != 13)
													{
														break;
													}
													fileData = GetFileData(ref TempFile);
													if (D_SC != 13)
													{
														break;
													}
													MyProject.Forms.Lead_Form.Delay.W_Data(1, Convert.ToByte(num8), (float)Conversion.Val(fileData));
													num8 = decimal.Add(num8, 1m);
													continue;
												}
												decimal num9 = decimal.Subtract(Gears.Value, 1m);
												decimal num10 = 1m;
												while (true)
												{
													if (ForLoopControl.ForNextCheckDec(num10, num9, 1m))
													{
														fileData = GetFileData(ref TempFile);
														if (Strings.Len(fileData) < 3 || D_SC != 13)
														{
															break;
														}
														fileData = GetFileData(ref TempFile);
														if (D_SC != 13)
														{
															break;
														}
														MyProject.Forms.Lead_Form.Delay.W_Data(2, Convert.ToByte(num10), (float)Conversion.Val(fileData));
														num10 = decimal.Add(num10, 1m);
														continue;
													}
													int num11 = 1;
													while (true)
													{
														fileData = GetFileData(ref TempFile);
														if (Strings.Len(fileData) < 3 || D_SC != 13)
														{
															break;
														}
														fileData = GetFileData(ref TempFile);
														if (D_SC != 13)
														{
															break;
														}
														MyProject.Forms.TCC_Form.MinTCC.W_Data((byte)num11, 1, (float)Conversion.Val(fileData));
														num11++;
														if (num11 <= 17)
														{
															continue;
														}
														int num12 = 1;
														while (true)
														{
															fileData = GetFileData(ref TempFile);
															if (Strings.Len(fileData) < 3 || D_SC != 13)
															{
																break;
															}
															fileData = GetFileData(ref TempFile);
															if (D_SC != 13)
															{
																break;
															}
															MyProject.Forms.TCC_Form.MinTCC.W_Data((byte)num12, 2, (float)Conversion.Val(fileData));
															num12++;
															if (num12 <= 17)
															{
																continue;
															}
															decimal value8 = Gears.Value;
															decimal num13 = 2m;
															while (ForLoopControl.ForNextCheckDec(num13, value8, 1m))
															{
																int grid_X = MyProject.Forms.TCC_Form.MinTCC.Grid_X;
																for (int i = 1; i <= grid_X; i++)
																{
																	MyProject.Forms.TCC_Form.MinTCC.W_Data((byte)i, Convert.ToByte(decimal.Subtract(decimal.Multiply(num13, 2m), 1m)), MyProject.Forms.TCC_Form.MinTCC.R_Data((byte)i, Convert.ToByte(decimal.Subtract(decimal.Multiply(decimal.Subtract(num13, 1m), 2m), 1m))));
																	MyProject.Forms.TCC_Form.MinTCC.W_Data((byte)i, Convert.ToByte(decimal.Multiply(num13, 2m)), MyProject.Forms.TCC_Form.MinTCC.R_Data((byte)i, Convert.ToByte(decimal.Multiply(decimal.Subtract(num13, 1m), 2m))));
																}
																num13 = decimal.Add(num13, 1m);
															}
															decimal value9 = Gears.Value;
															decimal num14 = 2m;
															while (true)
															{
																if (ForLoopControl.ForNextCheckDec(num14, value9, 1m))
																{
																	int num15 = 1;
																	while (true)
																	{
																		fileData = GetFileData(ref TempFile);
																		if (Strings.Len(fileData) < 3 || D_SC != 13)
																		{
																			break;
																		}
																		fileData = GetFileData(ref TempFile);
																		if (D_SC != 13)
																		{
																			break;
																		}
																		MyProject.Forms.TCC_Form.MinTCC.W_Data((byte)num15, Convert.ToByte(decimal.Subtract(decimal.Multiply(num14, 2m), 1m)), (float)Conversion.Val(fileData));
																		num15++;
																		if (num15 <= 17)
																		{
																			continue;
																		}
																		goto IL_199c;
																	}
																	break;
																}
																fileData = GetFileData(ref TempFile);
																if (Strings.Len(fileData) < 3 || D_SC != 13)
																{
																	break;
																}
																fileData = GetFileData(ref TempFile);
																if (D_SC != 13)
																{
																	break;
																}
																MyProject.Forms.TCC_Form.MinTCCrpm.Value = new decimal(Conversion.Val(fileData));
																fileData = GetFileData(ref TempFile);
																if (Strings.Len(fileData) < 3 || D_SC != 13)
																{
																	break;
																}
																fileData = GetFileData(ref TempFile);
																if (D_SC != 13)
																{
																	break;
																}
																MyProject.Forms.TCC_Form.MinTCCmintps.Value = new decimal(Conversion.Val(fileData));
																fileData = GetFileData(ref TempFile);
																if (Strings.Len(fileData) < 3 || D_SC != 13)
																{
																	break;
																}
																fileData = GetFileData(ref TempFile);
																if (D_SC != 13)
																{
																	break;
																}
																MyProject.Forms.TCC_Form.MinTCCmaxtps.Value = new decimal(Conversion.Val(fileData));
																fileData = GetFileData(ref TempFile);
																if (Strings.Len(fileData) < 3 || D_SC != 13)
																{
																	break;
																}
																fileData = GetFileData(ref TempFile);
																if (D_SC != 13)
																{
																	break;
																}
																if (Operators.CompareString(fileData, "1", false) == 0)
																{
																	SGS.Checked = true;
																}
																else
																{
																	SGS.Checked = false;
																}
																fileData = GetFileData(ref TempFile);
																if (Strings.Len(fileData) < 3 || D_SC != 13)
																{
																	break;
																}
																fileData = GetFileData(ref TempFile);
																if (D_SC != 13)
																{
																	break;
																}
																if (Operators.CompareString(fileData, "1", false) == 0)
																{
																	MyProject.Forms.Export_Form.CheckBox2.Checked = true;
																}
																else
																{
																	MyProject.Forms.Export_Form.CheckBox2.Checked = false;
																}
																fileData = GetFileData(ref TempFile);
																if (Strings.Len(fileData) < 3 || D_SC != 13)
																{
																	break;
																}
																fileData = GetFileData(ref TempFile);
																if (D_SC != 13)
																{
																	break;
																}
																if (Operators.CompareString(fileData, "1", false) == 0)
																{
																	MyProject.Forms.Export_Form.CheckBox3.Checked = true;
																}
																else
																{
																	MyProject.Forms.Export_Form.CheckBox3.Checked = false;
																}
																fileData = GetFileData(ref TempFile);
																if (Strings.Len(fileData) < 3 || D_SC != 13)
																{
																	break;
																}
																fileData = GetFileData(ref TempFile);
																if (D_SC != 13)
																{
																	break;
																}
																if (Operators.CompareString(fileData, "1", false) == 0)
																{
																	MyProject.Forms.Export_Form.CheckBox4.Checked = true;
																}
																else
																{
																	MyProject.Forms.Export_Form.CheckBox4.Checked = false;
																}
																fileData = GetFileData(ref TempFile);
																if (Strings.Len(fileData) < 3 || D_SC != 13)
																{
																	break;
																}
																fileData = GetFileData(ref TempFile);
																if (D_SC != 13)
																{
																	break;
																}
																if (Operators.CompareString(fileData, "1", false) == 0)
																{
																	MyProject.Forms.Export_Form.CheckBox5.Checked = true;
																}
																else
																{
																	MyProject.Forms.Export_Form.CheckBox5.Checked = false;
																}
																fileData = GetFileData(ref TempFile);
																if (Strings.Len(fileData) < 3 || D_SC != 13)
																{
																	break;
																}
																fileData = GetFileData(ref TempFile);
																if (D_SC != 13)
																{
																	break;
																}
																if (Operators.CompareString(fileData, "1", false) == 0)
																{
																	MyProject.Forms.Export_Form.CheckBox6.Checked = true;
																}
																else
																{
																	MyProject.Forms.Export_Form.CheckBox6.Checked = false;
																}
																fileData = GetFileData(ref TempFile);
																if (Strings.Len(fileData) < 3 || D_SC != 13)
																{
																	break;
																}
																fileData = GetFileData(ref TempFile);
																if (D_SC != 13)
																{
																	break;
																}
																if (Operators.CompareString(fileData, "1", false) == 0)
																{
																	MyProject.Forms.Export_Form.CheckBox7.Checked = true;
																}
																else
																{
																	MyProject.Forms.Export_Form.CheckBox7.Checked = false;
																}
																fileData = GetFileData(ref TempFile);
																if (Strings.Len(fileData) < 3 || D_SC != 13)
																{
																	break;
																}
																fileData = GetFileData(ref TempFile);
																if (D_SC != 13)
																{
																	break;
																}
																if (Operators.CompareString(fileData, "1", false) == 0)
																{
																	MyProject.Forms.Export_Form.CheckBox8.Checked = true;
																}
																else
																{
																	MyProject.Forms.Export_Form.CheckBox8.Checked = false;
																}
																fileData = GetFileData(ref TempFile);
																if (Strings.Len(fileData) < 3 || D_SC != 13)
																{
																	break;
																}
																fileData = GetFileData(ref TempFile);
																if (D_SC != 13)
																{
																	break;
																}
																if (Operators.CompareString(fileData, "1", false) == 0)
																{
																	MyProject.Forms.Export_Form.CheckBox9.Checked = true;
																}
																else
																{
																	MyProject.Forms.Export_Form.CheckBox9.Checked = false;
																}
																fileData = GetFileData(ref TempFile);
																if (Strings.Len(fileData) < 3 || D_SC != 13)
																{
																	break;
																}
																fileData = GetFileData(ref TempFile);
																if (D_SC != 13)
																{
																	break;
																}
																if (Operators.CompareString(fileData, "1", false) == 0)
																{
																	MyProject.Forms.Export_Form.CheckBox10.Checked = true;
																}
																else
																{
																	MyProject.Forms.Export_Form.CheckBox10.Checked = false;
																}
																fileData = GetFileData(ref TempFile);
																if (Strings.Len(fileData) < 3 || D_SC != 13)
																{
																	break;
																}
																fileData = GetFileData(ref TempFile);
																if (D_SC != 13)
																{
																	break;
																}
																if (Operators.CompareString(fileData, "1", false) == 0)
																{
																	MyProject.Forms.Export_Form.CheckBox11.Checked = true;
																}
																else
																{
																	MyProject.Forms.Export_Form.CheckBox11.Checked = false;
																}
																fileData = GetFileData(ref TempFile);
																if (Strings.Len(fileData) < 3 || D_SC != 13)
																{
																	break;
																}
																fileData = GetFileData(ref TempFile);
																if (D_SC != 13)
																{
																	break;
																}
																if (Operators.CompareString(fileData, "1", false) == 0)
																{
																	MyProject.Forms.Export_Form.CheckBox12.Checked = true;
																}
																else
																{
																	MyProject.Forms.Export_Form.CheckBox12.Checked = false;
																}
																fileData = GetFileData(ref TempFile);
																if (Strings.Len(fileData) < 3 || D_SC != 13)
																{
																	break;
																}
																fileData = GetFileData(ref TempFile);
																if (D_SC != 13)
																{
																	break;
																}
																if (Operators.CompareString(fileData, "1", false) == 0)
																{
																	MyProject.Forms.Export_Form.CheckBox13.Checked = true;
																}
																else
																{
																	MyProject.Forms.Export_Form.CheckBox13.Checked = false;
																}
																fileData = GetFileData(ref TempFile);
																if (Strings.Len(fileData) < 3 || D_SC != 13)
																{
																	break;
																}
																fileData = GetFileData(ref TempFile);
																if (D_SC != 13)
																{
																	break;
																}
																if (Operators.CompareString(fileData, "1", false) == 0)
																{
																	MyProject.Forms.Export_Form.CheckBox14.Checked = true;
																}
																else
																{
																	MyProject.Forms.Export_Form.CheckBox14.Checked = false;
																}
																fileData = GetFileData(ref TempFile);
																if (Strings.Len(fileData) < 3 || D_SC != 13)
																{
																	break;
																}
																fileData = GetFileData(ref TempFile);
																if (D_SC != 13)
																{
																	break;
																}
																if (Operators.CompareString(fileData, "1", false) == 0)
																{
																	MyProject.Forms.Export_Form.CheckBox15.Checked = true;
																}
																else
																{
																	MyProject.Forms.Export_Form.CheckBox15.Checked = false;
																}
																fileData = GetFileData(ref TempFile);
																if (Strings.Len(fileData) < 3 || D_SC != 13)
																{
																	break;
																}
																fileData = GetFileData(ref TempFile);
																if (D_SC != 13)
																{
																	break;
																}
																if (Operators.CompareString(fileData, "1", false) == 0)
																{
																	MyProject.Forms.Export_Form.CheckBox16.Checked = true;
																}
																else
																{
																	MyProject.Forms.Export_Form.CheckBox16.Checked = false;
																}
																fileData = GetFileData(ref TempFile);
																if (Strings.Len(fileData) < 3 || D_SC != 13)
																{
																	break;
																}
																fileData = GetFileData(ref TempFile);
																if (D_SC != 13)
																{
																	break;
																}
																if (Operators.CompareString(fileData, "1", false) == 0)
																{
																	MyProject.Forms.Export_Form.CheckBox17.Checked = true;
																}
																else
																{
																	MyProject.Forms.Export_Form.CheckBox17.Checked = false;
																}
																fileData = GetFileData(ref TempFile);
																if (Strings.Len(fileData) < 3 || D_SC != 13)
																{
																	break;
																}
																fileData = GetFileData(ref TempFile);
																if (D_SC != 13)
																{
																	break;
																}
																MyProject.Forms.Export_Form.ComboBox3.SelectedIndex = (int)Math.Round(Conversion.Val(fileData));
																fileData = GetFileData(ref TempFile);
																if (Strings.Len(fileData) < 3 || D_SC != 13)
																{
																	break;
																}
																fileData = GetFileData(ref TempFile);
																if (D_SC != 13)
																{
																	break;
																}
																MyProject.Forms.Export_Form.ComboBox4.SelectedIndex = (int)Math.Round(Conversion.Val(fileData));
																fileData = GetFileData(ref TempFile);
																if (Strings.Len(fileData) < 3 || D_SC != 13)
																{
																	break;
																}
																fileData = GetFileData(ref TempFile);
																if (D_SC != 13)
																{
																	break;
																}
																MyProject.Forms.Export_Form.Gear.Value = new decimal(Conversion.Val(fileData));
																fileData = GetFileData(ref TempFile);
																if (Strings.Len(fileData) < 3 || D_SC != 13)
																{
																	break;
																}
																fileData = GetFileData(ref TempFile);
																if (D_SC != 13)
																{
																	break;
																}
																MyProject.Forms.Export_Form.NDTire.Value = new decimal(Conversion.Val(fileData));
																fileData = GetFileData(ref TempFile);
																if (Strings.Len(fileData) < 3 || D_SC != 13)
																{
																	break;
																}
																fileData = GetFileData(ref TempFile);
																if (D_SC != 13)
																{
																	break;
																}
																if (Operators.CompareString(fileData, "1", false) == 0)
																{
																	OverRide_Enable.Checked = true;
																}
																else
																{
																	OverRide_Enable.Checked = false;
																}
																decimal num16 = decimal.Multiply(decimal.Subtract(Gears.Value, 1m), 2m);
																decimal num17 = 1m;
																while (true)
																{
																	if (ForLoopControl.ForNextCheckDec(num17, num16, 1m))
																	{
																		int num18 = 1;
																		while (true)
																		{
																			fileData = GetFileData(ref TempFile);
																			if (Strings.Len(fileData) < 3 || D_SC != 13)
																			{
																				break;
																			}
																			fileData = GetFileData(ref TempFile);
																			if (D_SC != 13)
																			{
																				break;
																			}
																			MyProject.Forms.OverRide_Form.OverRide_Grid.W_Data((byte)num18, Convert.ToByte(num17), (float)Conversion.Val(fileData));
																			num18++;
																			if (num18 <= 17)
																			{
																				continue;
																			}
																			goto IL_2522;
																		}
																		break;
																	}
																	fileData = GetFileData(ref TempFile);
																	if (Strings.Len(fileData) < 3 || D_SC != 13)
																	{
																		break;
																	}
																	fileData = GetFileData(ref TempFile);
																	if (D_SC != 13)
																	{
																		break;
																	}
																	if (Operators.CompareString(fileData, "1", false) == 0)
																	{
																		MyProject.Forms.Export_Form.CheckBox18.Checked = true;
																	}
																	else
																	{
																		MyProject.Forms.Export_Form.CheckBox18.Checked = false;
																	}
																	fileData = GetFileData(ref TempFile);
																	if (Strings.Len(fileData) < 3 || D_SC != 13)
																	{
																		break;
																	}
																	fileData = GetFileData(ref TempFile);
																	if (D_SC != 13)
																	{
																		break;
																	}
																	if (Operators.CompareString(fileData, "1", false) == 0)
																	{
																		MyProject.Forms.Export_Form.CheckBox19.Checked = true;
																	}
																	else
																	{
																		MyProject.Forms.Export_Form.CheckBox19.Checked = false;
																	}
																	fileData = GetFileData(ref TempFile);
																	if (Strings.Len(fileData) < 3 || D_SC != 13)
																	{
																		break;
																	}
																	fileData = GetFileData(ref TempFile);
																	if (D_SC != 13)
																	{
																		break;
																	}
																	if (Operators.CompareString(fileData, "1", false) == 0)
																	{
																		MyProject.Forms.Export_Form.CheckBox20.Checked = true;
																	}
																	else
																	{
																		MyProject.Forms.Export_Form.CheckBox20.Checked = false;
																	}
																	fileData = GetFileData(ref TempFile);
																	if (Strings.Len(fileData) < 3 || D_SC != 13)
																	{
																		break;
																	}
																	fileData = GetFileData(ref TempFile);
																	if (D_SC != 13)
																	{
																		break;
																	}
																	if (Operators.CompareString(fileData, "1", false) == 0)
																	{
																		RRM.Checked = true;
																	}
																	else
																	{
																		RRM.Checked = false;
																	}
																	fileData = GetFileData(ref TempFile);
																	if (Strings.Len(fileData) < 3 || D_SC != 13)
																	{
																		break;
																	}
																	fileData = GetFileData(ref TempFile);
																	if (D_SC != 13)
																	{
																		break;
																	}
																	if (Operators.CompareString(fileData, "1", false) == 0)
																	{
																		MyProject.Forms.Export_Form.CheckBox21.Checked = true;
																	}
																	else
																	{
																		MyProject.Forms.Export_Form.CheckBox21.Checked = false;
																	}
																	fileData = GetFileData(ref TempFile);
																	if (Strings.Len(fileData) < 3 || D_SC != 13)
																	{
																		break;
																	}
																	fileData = GetFileData(ref TempFile);
																	if (D_SC == 13)
																	{
																		if (Operators.CompareString(fileData, "1", false) == 0)
																		{
																			WOTTCCPrep.Checked = true;
																		}
																		else
																		{
																			WOTTCCPrep.Checked = false;
																		}
																	}
																	break;
																	IL_2522:
																	num17 = decimal.Add(num17, 1m);
																}
																break;
																IL_1a14:
																num14 = decimal.Add(num14, 1m);
																continue;
																IL_199c:
																int num19 = 1;
																while (true)
																{
																	fileData = GetFileData(ref TempFile);
																	if (Strings.Len(fileData) < 3 || D_SC != 13)
																	{
																		break;
																	}
																	fileData = GetFileData(ref TempFile);
																	if (D_SC != 13)
																	{
																		break;
																	}
																	MyProject.Forms.TCC_Form.MinTCC.W_Data((byte)num19, Convert.ToByte(decimal.Multiply(num14, 2m)), (float)Conversion.Val(fileData));
																	num19++;
																	if (num19 <= 17)
																	{
																		continue;
																	}
																	goto IL_1a14;
																}
																break;
															}
															break;
														}
														break;
													}
													break;
												}
												break;
											}
											break;
										}
										break;
									}
								}
							}
						}
					}
				}
			}
			TempFile.Close();
		}
	}

	private string GetFileData(ref StreamReader TempFile)
	{
		checked
		{
			do
			{
				string text = "";
				byte b;
				do
				{
					b = (byte)TempFile.Read();
					switch (b)
					{
					case 9:
						D_SC = 9;
						break;
					case 13:
						D_SC = 13;
						break;
					default:
						text += Conversions.ToString(Strings.Chr(unchecked((int)b)));
						continue;
					case 10:
						continue;
					}
					break;
				}
				while (!TempFile.EndOfStream);
				if (Operators.CompareString(text, "", false) == 0)
				{
					continue;
				}
				if (b == 9)
				{
					b = (byte)TempFile.Peek();
					if (b == 13)
					{
						b = (byte)TempFile.Read();
						D_SC = 13;
					}
				}
				return text;
			}
			while (!TempFile.EndOfStream);
			return "";
		}
	}

	private void PutFileData(ref StreamWriter TempFile, string TempS)
	{
		int num = Strings.Len(TempS);
		for (int i = 1; i <= num; i = checked(i + 1))
		{
			byte b = checked((byte)Strings.Asc(Strings.Mid(TempS, i, 1)));
			TempFile.Write(Strings.Chr((int)b));
		}
	}

	private void Main_Form_Shown(object sender, EventArgs e)
	{
		Init = 1;
	}

	private void TireCalc_Click(object sender, EventArgs e)
	{
		((Control)MyProject.Forms.Tire_Form).Show();
		((Form)MyProject.Forms.Tire_Form).WindowState = (FormWindowState)0;
		((Control)MyProject.Forms.Tire_Form).Focus();
	}
}
