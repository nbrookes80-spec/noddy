using System;
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
public class Export_Form : Form
{
	public struct table_type
	{
		public byte v;

		public string nm;

		public int fw;

		public ushort tn;

		public string units;

		public int table_x;

		public int table_y;

		public float[,] table;

		public string xunits;

		public string[] xaxis;

		public string yunits;

		public string[] yaxis;
	}

	private IContainer components;

	[AccessedThroughProperty("ToolTip1")]
	private ToolTip _ToolTip1;

	[AccessedThroughProperty("GroupBox3")]
	private GroupBox _GroupBox3;

	[AccessedThroughProperty("GroupBox2")]
	private GroupBox _GroupBox2;

	[AccessedThroughProperty("Export_Grid")]
	private BCGridControl _Export_Grid;

	[AccessedThroughProperty("Label7")]
	private Label _Label7;

	[AccessedThroughProperty("Button3")]
	private Button _Button3;

	[AccessedThroughProperty("Button2")]
	private Button _Button2;

	[AccessedThroughProperty("Label6")]
	private Label _Label6;

	[AccessedThroughProperty("Button1")]
	private Button _Button1;

	[AccessedThroughProperty("GroupBox1")]
	private GroupBox _GroupBox1;

	[AccessedThroughProperty("Label5")]
	private Label _Label5;

	[AccessedThroughProperty("TextBox5")]
	private TextBox _TextBox5;

	[AccessedThroughProperty("Label4")]
	private Label _Label4;

	[AccessedThroughProperty("TextBox4")]
	private TextBox _TextBox4;

	[AccessedThroughProperty("Label3")]
	private Label _Label3;

	[AccessedThroughProperty("TextBox3")]
	private TextBox _TextBox3;

	[AccessedThroughProperty("Label2")]
	private Label _Label2;

	[AccessedThroughProperty("TextBox2")]
	private TextBox _TextBox2;

	[AccessedThroughProperty("Label1")]
	private Label _Label1;

	[AccessedThroughProperty("TextBox1")]
	private TextBox _TextBox1;

	[AccessedThroughProperty("ComboBox2")]
	private ComboBox _ComboBox2;

	[AccessedThroughProperty("GroupBox4")]
	private GroupBox _GroupBox4;

	[AccessedThroughProperty("CheckBox3")]
	private CheckBox _CheckBox3;

	[AccessedThroughProperty("CheckBox2")]
	private CheckBox _CheckBox2;

	[AccessedThroughProperty("CheckBox7")]
	private CheckBox _CheckBox7;

	[AccessedThroughProperty("CheckBox6")]
	private CheckBox _CheckBox6;

	[AccessedThroughProperty("CheckBox5")]
	private CheckBox _CheckBox5;

	[AccessedThroughProperty("CheckBox4")]
	private CheckBox _CheckBox4;

	[AccessedThroughProperty("Button4")]
	private Button _Button4;

	[AccessedThroughProperty("CheckBox9")]
	private CheckBox _CheckBox9;

	[AccessedThroughProperty("CheckBox8")]
	private CheckBox _CheckBox8;

	[AccessedThroughProperty("SaveFileDialog1")]
	private SaveFileDialog _SaveFileDialog1;

	[AccessedThroughProperty("GroupBox5")]
	private GroupBox _GroupBox5;

	[AccessedThroughProperty("CheckBox1")]
	private CheckBox _CheckBox1;

	[AccessedThroughProperty("ComboBox1")]
	private ComboBox _ComboBox1;

	[AccessedThroughProperty("CheckBox12")]
	private CheckBox _CheckBox12;

	[AccessedThroughProperty("CheckBox11")]
	private CheckBox _CheckBox11;

	[AccessedThroughProperty("CheckBox10")]
	private CheckBox _CheckBox10;

	[AccessedThroughProperty("CheckBox13")]
	private CheckBox _CheckBox13;

	[AccessedThroughProperty("CheckBox14")]
	private CheckBox _CheckBox14;

	[AccessedThroughProperty("Label8")]
	private Label _Label8;

	[AccessedThroughProperty("CheckBox15")]
	private CheckBox _CheckBox15;

	[AccessedThroughProperty("Gear")]
	private NumericUpDown _Gear;

	[AccessedThroughProperty("CheckBox16")]
	private CheckBox _CheckBox16;

	[AccessedThroughProperty("ComboBox3")]
	private ComboBox _ComboBox3;

	[AccessedThroughProperty("ComboBox4")]
	private ComboBox _ComboBox4;

	[AccessedThroughProperty("GroupBox6")]
	private GroupBox _GroupBox6;

	[AccessedThroughProperty("CheckBox17")]
	private CheckBox _CheckBox17;

	[AccessedThroughProperty("NDTire")]
	private NumericUpDown _NDTire;

	[AccessedThroughProperty("CheckBox20")]
	private CheckBox _CheckBox20;

	[AccessedThroughProperty("CheckBox18")]
	private CheckBox _CheckBox18;

	[AccessedThroughProperty("CheckBox19")]
	private CheckBox _CheckBox19;

	[AccessedThroughProperty("CheckBox21")]
	private CheckBox _CheckBox21;

	public byte EMD;

	public byte EMD_MAX;

	public ushort Init;

	private int[][] VSSOptions;

	private int[] ExportAllowed;

	private bool ms_active;

	private bool ms_DM;

	private bool ms_RRM;

	private bool ms_SGS;

	private decimal ms_Gear;

	private decimal ms_DRPM;

	private decimal ms_Factor;

	private decimal ms_Offset;

	private decimal ms_UpF;

	private decimal ms_DownF;

	private decimal ms_WotLck;

	private int ms_SlopeCombo;

	private float[] ms_RPM;

	private float[,] ms_MinTCC;

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

	internal virtual BCGridControl Export_Grid
	{
		[DebuggerNonUserCode]
		get
		{
			return _Export_Grid;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_Export_Grid = value;
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

	internal virtual Button Button3
	{
		[DebuggerNonUserCode]
		get
		{
			return _Button3;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = Button3_Click;
			if (_Button3 != null)
			{
				((Control)_Button3).Click -= eventHandler;
			}
			_Button3 = value;
			if (_Button3 != null)
			{
				((Control)_Button3).Click += eventHandler;
			}
		}
	}

	internal virtual Button Button2
	{
		[DebuggerNonUserCode]
		get
		{
			return _Button2;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = Button2_Click;
			if (_Button2 != null)
			{
				((Control)_Button2).Click -= eventHandler;
			}
			_Button2 = value;
			if (_Button2 != null)
			{
				((Control)_Button2).Click += eventHandler;
			}
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

	internal virtual Button Button1
	{
		[DebuggerNonUserCode]
		get
		{
			return _Button1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = Button1_Click;
			if (_Button1 != null)
			{
				((Control)_Button1).Click -= eventHandler;
			}
			_Button1 = value;
			if (_Button1 != null)
			{
				((Control)_Button1).Click += eventHandler;
			}
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

	internal virtual TextBox TextBox5
	{
		[DebuggerNonUserCode]
		get
		{
			return _TextBox5;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_TextBox5 = value;
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

	internal virtual TextBox TextBox4
	{
		[DebuggerNonUserCode]
		get
		{
			return _TextBox4;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_TextBox4 = value;
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

	internal virtual TextBox TextBox3
	{
		[DebuggerNonUserCode]
		get
		{
			return _TextBox3;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_TextBox3 = value;
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

	internal virtual TextBox TextBox2
	{
		[DebuggerNonUserCode]
		get
		{
			return _TextBox2;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_TextBox2 = value;
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

	internal virtual TextBox TextBox1
	{
		[DebuggerNonUserCode]
		get
		{
			return _TextBox1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_TextBox1 = value;
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
			//IL_0016: Unknown result type (might be due to invalid IL or missing references)
			//IL_001c: Expected O, but got Unknown
			EventHandler eventHandler = ComboBox2_SelectedIndexChanged;
			DrawItemEventHandler val = new DrawItemEventHandler(ComboBox2_DrawItem);
			if (_ComboBox2 != null)
			{
				_ComboBox2.SelectedIndexChanged -= eventHandler;
				_ComboBox2.DrawItem -= val;
			}
			_ComboBox2 = value;
			if (_ComboBox2 != null)
			{
				_ComboBox2.SelectedIndexChanged += eventHandler;
				_ComboBox2.DrawItem += val;
			}
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

	internal virtual CheckBox CheckBox3
	{
		[DebuggerNonUserCode]
		get
		{
			return _CheckBox3;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_CheckBox3 = value;
		}
	}

	internal virtual CheckBox CheckBox2
	{
		[DebuggerNonUserCode]
		get
		{
			return _CheckBox2;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_CheckBox2 = value;
		}
	}

	internal virtual CheckBox CheckBox7
	{
		[DebuggerNonUserCode]
		get
		{
			return _CheckBox7;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_CheckBox7 = value;
		}
	}

	internal virtual CheckBox CheckBox6
	{
		[DebuggerNonUserCode]
		get
		{
			return _CheckBox6;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_CheckBox6 = value;
		}
	}

	internal virtual CheckBox CheckBox5
	{
		[DebuggerNonUserCode]
		get
		{
			return _CheckBox5;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_CheckBox5 = value;
		}
	}

	internal virtual CheckBox CheckBox4
	{
		[DebuggerNonUserCode]
		get
		{
			return _CheckBox4;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_CheckBox4 = value;
		}
	}

	internal virtual Button Button4
	{
		[DebuggerNonUserCode]
		get
		{
			return _Button4;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = EF;
			if (_Button4 != null)
			{
				((Control)_Button4).Click -= eventHandler;
			}
			_Button4 = value;
			if (_Button4 != null)
			{
				((Control)_Button4).Click += eventHandler;
			}
		}
	}

	internal virtual CheckBox CheckBox9
	{
		[DebuggerNonUserCode]
		get
		{
			return _CheckBox9;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_CheckBox9 = value;
		}
	}

	internal virtual CheckBox CheckBox8
	{
		[DebuggerNonUserCode]
		get
		{
			return _CheckBox8;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = CheckBox8_CheckedChanged;
			if (_CheckBox8 != null)
			{
				_CheckBox8.CheckedChanged -= eventHandler;
			}
			_CheckBox8 = value;
			if (_CheckBox8 != null)
			{
				_CheckBox8.CheckedChanged += eventHandler;
			}
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
			//IL_0016: Unknown result type (might be due to invalid IL or missing references)
			//IL_001c: Expected O, but got Unknown
			EventHandler eventHandler = ComboBox1_SelectedIndexChanged;
			DrawItemEventHandler val = new DrawItemEventHandler(ComboBox1_DrawItem);
			if (_ComboBox1 != null)
			{
				_ComboBox1.SelectedIndexChanged -= eventHandler;
				_ComboBox1.DrawItem -= val;
			}
			_ComboBox1 = value;
			if (_ComboBox1 != null)
			{
				_ComboBox1.SelectedIndexChanged += eventHandler;
				_ComboBox1.DrawItem += val;
			}
		}
	}

	internal virtual CheckBox CheckBox12
	{
		[DebuggerNonUserCode]
		get
		{
			return _CheckBox12;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = CheckBox12_CheckedChanged;
			if (_CheckBox12 != null)
			{
				_CheckBox12.CheckedChanged -= eventHandler;
			}
			_CheckBox12 = value;
			if (_CheckBox12 != null)
			{
				_CheckBox12.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual CheckBox CheckBox11
	{
		[DebuggerNonUserCode]
		get
		{
			return _CheckBox11;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = CheckBox11_CheckedChanged;
			if (_CheckBox11 != null)
			{
				_CheckBox11.CheckedChanged -= eventHandler;
			}
			_CheckBox11 = value;
			if (_CheckBox11 != null)
			{
				_CheckBox11.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual CheckBox CheckBox10
	{
		[DebuggerNonUserCode]
		get
		{
			return _CheckBox10;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_CheckBox10 = value;
		}
	}

	internal virtual CheckBox CheckBox13
	{
		[DebuggerNonUserCode]
		get
		{
			return _CheckBox13;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_CheckBox13 = value;
		}
	}

	internal virtual CheckBox CheckBox14
	{
		[DebuggerNonUserCode]
		get
		{
			return _CheckBox14;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_CheckBox14 = value;
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

	internal virtual CheckBox CheckBox15
	{
		[DebuggerNonUserCode]
		get
		{
			return _CheckBox15;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_CheckBox15 = value;
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
			_Gear = value;
		}
	}

	internal virtual CheckBox CheckBox16
	{
		[DebuggerNonUserCode]
		get
		{
			return _CheckBox16;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_CheckBox16 = value;
		}
	}

	internal virtual ComboBox ComboBox3
	{
		[DebuggerNonUserCode]
		get
		{
			return _ComboBox3;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_ComboBox3 = value;
		}
	}

	internal virtual ComboBox ComboBox4
	{
		[DebuggerNonUserCode]
		get
		{
			return _ComboBox4;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_ComboBox4 = value;
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

	internal virtual CheckBox CheckBox17
	{
		[DebuggerNonUserCode]
		get
		{
			return _CheckBox17;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = CheckBox17_CheckedChanged;
			if (_CheckBox17 != null)
			{
				_CheckBox17.CheckedChanged -= eventHandler;
			}
			_CheckBox17 = value;
			if (_CheckBox17 != null)
			{
				_CheckBox17.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual NumericUpDown NDTire
	{
		[DebuggerNonUserCode]
		get
		{
			return _NDTire;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = NDTire_ValueChanged;
			if (_NDTire != null)
			{
				_NDTire.ValueChanged -= eventHandler;
			}
			_NDTire = value;
			if (_NDTire != null)
			{
				_NDTire.ValueChanged += eventHandler;
			}
		}
	}

	internal virtual CheckBox CheckBox20
	{
		[DebuggerNonUserCode]
		get
		{
			return _CheckBox20;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_CheckBox20 = value;
		}
	}

	internal virtual CheckBox CheckBox18
	{
		[DebuggerNonUserCode]
		get
		{
			return _CheckBox18;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_CheckBox18 = value;
		}
	}

	internal virtual CheckBox CheckBox19
	{
		[DebuggerNonUserCode]
		get
		{
			return _CheckBox19;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_CheckBox19 = value;
		}
	}

	internal virtual CheckBox CheckBox21
	{
		[DebuggerNonUserCode]
		get
		{
			return _CheckBox21;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = CheckBox21_CheckedChanged;
			if (_CheckBox21 != null)
			{
				_CheckBox21.CheckedChanged -= eventHandler;
			}
			_CheckBox21 = value;
			if (_CheckBox21 != null)
			{
				_CheckBox21.CheckedChanged += eventHandler;
			}
		}
	}

	public Export_Form()
	{
		((Form)this).Load += Export_Form_Load;
		((Form)this).Shown += Export_Form_Shown;
		((Form)this).Closing += Form_Closing;
		EMD = 1;
		EMD_MAX = 1;
		Init = 0;
		VSSOptions = new int[8][]
		{
			new int[0],
			new int[4] { 2, 0, 1, 3 },
			new int[2] { 4, 5 },
			new int[1] { 4 },
			new int[1] { 4 },
			new int[1] { 4 },
			new int[1] { 4 },
			new int[1] { 4 }
		};
		ExportAllowed = new int[0];
		ms_active = false;
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
		//IL_0038: Unknown result type (might be due to invalid IL or missing references)
		//IL_0042: Expected O, but got Unknown
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
		//IL_00b1: Unknown result type (might be due to invalid IL or missing references)
		//IL_00bb: Expected O, but got Unknown
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
		//IL_011f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0129: Expected O, but got Unknown
		//IL_012a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0134: Expected O, but got Unknown
		//IL_0135: Unknown result type (might be due to invalid IL or missing references)
		//IL_013f: Expected O, but got Unknown
		//IL_0140: Unknown result type (might be due to invalid IL or missing references)
		//IL_014a: Expected O, but got Unknown
		//IL_014b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0155: Expected O, but got Unknown
		//IL_0156: Unknown result type (might be due to invalid IL or missing references)
		//IL_0160: Expected O, but got Unknown
		//IL_0161: Unknown result type (might be due to invalid IL or missing references)
		//IL_016b: Expected O, but got Unknown
		//IL_016c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0176: Expected O, but got Unknown
		//IL_0177: Unknown result type (might be due to invalid IL or missing references)
		//IL_0181: Expected O, but got Unknown
		//IL_0182: Unknown result type (might be due to invalid IL or missing references)
		//IL_018c: Expected O, but got Unknown
		//IL_018d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0197: Expected O, but got Unknown
		//IL_0198: Unknown result type (might be due to invalid IL or missing references)
		//IL_01a2: Expected O, but got Unknown
		//IL_01a3: Unknown result type (might be due to invalid IL or missing references)
		//IL_01ad: Expected O, but got Unknown
		//IL_01ae: Unknown result type (might be due to invalid IL or missing references)
		//IL_01b8: Expected O, but got Unknown
		//IL_01b9: Unknown result type (might be due to invalid IL or missing references)
		//IL_01c3: Expected O, but got Unknown
		//IL_01c4: Unknown result type (might be due to invalid IL or missing references)
		//IL_01ce: Expected O, but got Unknown
		//IL_01cf: Unknown result type (might be due to invalid IL or missing references)
		//IL_01d9: Expected O, but got Unknown
		//IL_01da: Unknown result type (might be due to invalid IL or missing references)
		//IL_01e4: Expected O, but got Unknown
		//IL_01e5: Unknown result type (might be due to invalid IL or missing references)
		//IL_01ef: Expected O, but got Unknown
		//IL_01f0: Unknown result type (might be due to invalid IL or missing references)
		//IL_01fa: Expected O, but got Unknown
		//IL_01fb: Unknown result type (might be due to invalid IL or missing references)
		//IL_0205: Expected O, but got Unknown
		//IL_0206: Unknown result type (might be due to invalid IL or missing references)
		//IL_0210: Expected O, but got Unknown
		//IL_0211: Unknown result type (might be due to invalid IL or missing references)
		//IL_021b: Expected O, but got Unknown
		//IL_021c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0226: Expected O, but got Unknown
		//IL_0227: Unknown result type (might be due to invalid IL or missing references)
		//IL_0231: Expected O, but got Unknown
		//IL_0232: Unknown result type (might be due to invalid IL or missing references)
		//IL_023c: Expected O, but got Unknown
		//IL_023d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0247: Expected O, but got Unknown
		//IL_0248: Unknown result type (might be due to invalid IL or missing references)
		//IL_0252: Expected O, but got Unknown
		//IL_0253: Unknown result type (might be due to invalid IL or missing references)
		//IL_025d: Expected O, but got Unknown
		//IL_025e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0268: Expected O, but got Unknown
		//IL_0a9f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0aa9: Expected O, but got Unknown
		//IL_22ff: Unknown result type (might be due to invalid IL or missing references)
		//IL_2309: Expected O, but got Unknown
		components = new Container();
		ComponentResourceManager componentResourceManager = new ComponentResourceManager(typeof(Export_Form));
		ToolTip1 = new ToolTip(components);
		CheckBox15 = new CheckBox();
		CheckBox16 = new CheckBox();
		ComboBox3 = new ComboBox();
		ComboBox4 = new ComboBox();
		Gear = new NumericUpDown();
		CheckBox21 = new CheckBox();
		CheckBox18 = new CheckBox();
		CheckBox19 = new CheckBox();
		CheckBox20 = new CheckBox();
		GroupBox3 = new GroupBox();
		GroupBox2 = new GroupBox();
		Export_Grid = new BCGridControl();
		Label7 = new Label();
		Button3 = new Button();
		Button2 = new Button();
		Label6 = new Label();
		Button1 = new Button();
		GroupBox1 = new GroupBox();
		Label5 = new Label();
		TextBox5 = new TextBox();
		Label4 = new Label();
		TextBox4 = new TextBox();
		Label3 = new Label();
		TextBox3 = new TextBox();
		Label2 = new Label();
		TextBox2 = new TextBox();
		Label1 = new Label();
		TextBox1 = new TextBox();
		ComboBox2 = new ComboBox();
		GroupBox4 = new GroupBox();
		GroupBox6 = new GroupBox();
		NDTire = new NumericUpDown();
		CheckBox17 = new CheckBox();
		Label8 = new Label();
		CheckBox14 = new CheckBox();
		CheckBox13 = new CheckBox();
		CheckBox12 = new CheckBox();
		CheckBox11 = new CheckBox();
		CheckBox10 = new CheckBox();
		Button4 = new Button();
		CheckBox9 = new CheckBox();
		CheckBox8 = new CheckBox();
		CheckBox7 = new CheckBox();
		CheckBox6 = new CheckBox();
		CheckBox5 = new CheckBox();
		CheckBox4 = new CheckBox();
		CheckBox3 = new CheckBox();
		CheckBox2 = new CheckBox();
		SaveFileDialog1 = new SaveFileDialog();
		GroupBox5 = new GroupBox();
		CheckBox1 = new CheckBox();
		ComboBox1 = new ComboBox();
		((ISupportInitialize)Gear).BeginInit();
		((Control)GroupBox3).SuspendLayout();
		((Control)GroupBox2).SuspendLayout();
		((Control)GroupBox1).SuspendLayout();
		((Control)GroupBox4).SuspendLayout();
		((Control)GroupBox6).SuspendLayout();
		((ISupportInitialize)NDTire).BeginInit();
		((Control)GroupBox5).SuspendLayout();
		((Control)this).SuspendLayout();
		ToolTip1.AutomaticDelay = 25000;
		ToolTip1.AutoPopDelay = 25000;
		ToolTip1.InitialDelay = 1000;
		ToolTip1.ReshowDelay = 1000;
		((ButtonBase)CheckBox15).AutoSize = true;
		CheckBox checkBox = CheckBox15;
		Point location = new Point(451, 63);
		((Control)checkBox).Location = location;
		((Control)CheckBox15).Name = "CheckBox15";
		CheckBox checkBox2 = CheckBox15;
		Size size = new Size(124, 17);
		((Control)checkBox2).Size = size;
		((Control)CheckBox15).TabIndex = 16;
		((ButtonBase)CheckBox15).Text = "HPT Unit Bug - ECM";
		ToolTip1.SetToolTip((Control)(object)CheckBox15, componentResourceManager.GetString("CheckBox15.ToolTip"));
		((ButtonBase)CheckBox15).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox16).AutoSize = true;
		CheckBox checkBox3 = CheckBox16;
		location = new Point(451, 86);
		((Control)checkBox3).Location = location;
		((Control)CheckBox16).Name = "CheckBox16";
		CheckBox checkBox4 = CheckBox16;
		size = new Size(124, 17);
		((Control)checkBox4).Size = size;
		((Control)CheckBox16).TabIndex = 18;
		((ButtonBase)CheckBox16).Text = "HPT Unit Bug - TCM";
		ToolTip1.SetToolTip((Control)(object)CheckBox16, componentResourceManager.GetString("CheckBox16.ToolTip"));
		((ButtonBase)CheckBox16).UseVisualStyleBackColor = true;
		ComboBox3.DropDownStyle = (ComboBoxStyle)2;
		((ListControl)ComboBox3).FormattingEnabled = true;
		ComboBox3.Items.AddRange(new object[5] { "(No Changes)", "Tow/Haul", "Dyno Mode", "Roll Race Mode", "Second Gear Start" });
		ComboBox comboBox = ComboBox3;
		location = new Point(241, 65);
		((Control)comboBox).Location = location;
		((Control)ComboBox3).Name = "ComboBox3";
		ComboBox comboBox2 = ComboBox3;
		size = new Size(163, 21);
		((Control)comboBox2).Size = size;
		((Control)ComboBox3).TabIndex = 19;
		ToolTip1.SetToolTip((Control)(object)ComboBox3, "Auto modifications to current settings. Keeps from having seperate full files for each mode when using common setups.");
		ComboBox4.DropDownStyle = (ComboBoxStyle)2;
		((ListControl)ComboBox4).FormattingEnabled = true;
		ComboBox4.Items.AddRange(new object[5] { "(No Changes)", "Tow/Haul", "Dyno Mode", "Roll Race Mode", "Second Gear Start" });
		ComboBox comboBox3 = ComboBox4;
		location = new Point(241, 115);
		((Control)comboBox3).Location = location;
		((Control)ComboBox4).Name = "ComboBox4";
		ComboBox comboBox4 = ComboBox4;
		size = new Size(163, 21);
		((Control)comboBox4).Size = size;
		((Control)ComboBox4).TabIndex = 20;
		ToolTip1.SetToolTip((Control)(object)ComboBox4, "Auto modifications to current settings. Keeps from having seperate full files for each mode when using common setups.");
		Gear.DecimalPlaces = 2;
		NumericUpDown gear = Gear;
		decimal increment = new decimal(new int[4] { 1, 0, 0, 131072 });
		gear.Increment = increment;
		NumericUpDown gear2 = Gear;
		location = new Point(388, 185);
		((Control)gear2).Location = location;
		increment = (Gear.Maximum = new decimal(new int[4] { 50, 0, 0, 0 }));
		increment = (Gear.Minimum = new decimal(new int[4] { 1, 0, 0, 65536 }));
		((Control)Gear).Name = "Gear";
		NumericUpDown gear3 = Gear;
		size = new Size(48, 20);
		((Control)gear3).Size = size;
		((Control)Gear).TabIndex = 17;
		ToolTip1.SetToolTip((Control)(object)Gear, "Transfercase ratio in low range.");
		increment = (Gear.Value = new decimal(new int[4] { 272, 0, 0, 131072 }));
		((ButtonBase)CheckBox21).AutoSize = true;
		CheckBox checkBox5 = CheckBox21;
		location = new Point(517, 21);
		((Control)checkBox5).Location = location;
		((Control)CheckBox21).Name = "CheckBox21";
		CheckBox checkBox6 = CheckBox21;
		size = new Size(129, 17);
		((Control)checkBox6).Size = size;
		((Control)CheckBox21).TabIndex = 9;
		((ButtonBase)CheckBox21).Text = "Export Always on Top";
		ToolTip1.SetToolTip((Control)(object)CheckBox21, "Forces window on top for easier access during manual copy.");
		((ButtonBase)CheckBox21).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox18).AutoSize = true;
		CheckBox18.Checked = true;
		CheckBox18.CheckState = (CheckState)1;
		CheckBox checkBox7 = CheckBox18;
		location = new Point(218, 142);
		((Control)checkBox7).Location = location;
		((Control)CheckBox18).Name = "CheckBox18";
		CheckBox checkBox8 = CheckBox18;
		size = new Size(115, 17);
		((Control)checkBox8).Size = size;
		((Control)CheckBox18).TabIndex = 22;
		((ButtonBase)CheckBox18).Text = "Export to Pattern C";
		((ButtonBase)CheckBox18).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox19).AutoSize = true;
		CheckBox checkBox9 = CheckBox19;
		location = new Point(451, 109);
		((Control)checkBox9).Location = location;
		((Control)CheckBox19).Name = "CheckBox19";
		CheckBox checkBox10 = CheckBox19;
		size = new Size(100, 17);
		((Control)checkBox10).Size = size;
		((Control)CheckBox19).TabIndex = 23;
		((ButtonBase)CheckBox19).Text = "Export TCC Min";
		((ButtonBase)CheckBox19).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox20).AutoSize = true;
		CheckBox checkBox11 = CheckBox20;
		location = new Point(451, 132);
		((Control)checkBox11).Location = location;
		((Control)CheckBox20).Name = "CheckBox20";
		CheckBox checkBox12 = CheckBox20;
		size = new Size(111, 17);
		((Control)checkBox12).Size = size;
		((Control)CheckBox20).TabIndex = 24;
		((ButtonBase)CheckBox20).Text = "Export VSS Count";
		((ButtonBase)CheckBox20).UseVisualStyleBackColor = true;
		((Control)GroupBox3).Controls.Add((Control)(object)GroupBox2);
		((Control)GroupBox3).Controls.Add((Control)(object)GroupBox1);
		GroupBox groupBox = GroupBox3;
		location = new Point(12, 62);
		((Control)groupBox).Location = location;
		((Control)GroupBox3).Name = "GroupBox3";
		GroupBox groupBox2 = GroupBox3;
		size = new Size(654, 280);
		((Control)groupBox2).Size = size;
		((Control)GroupBox3).TabIndex = 3;
		GroupBox3.TabStop = false;
		GroupBox3.Text = "Manual Export";
		((Control)GroupBox2).Controls.Add((Control)(object)Export_Grid);
		((Control)GroupBox2).Controls.Add((Control)(object)Label7);
		((Control)GroupBox2).Controls.Add((Control)(object)Button3);
		((Control)GroupBox2).Controls.Add((Control)(object)Button2);
		((Control)GroupBox2).Controls.Add((Control)(object)Label6);
		((Control)GroupBox2).Controls.Add((Control)(object)Button1);
		GroupBox groupBox3 = GroupBox2;
		location = new Point(205, 16);
		((Control)groupBox3).Location = location;
		((Control)GroupBox2).Name = "GroupBox2";
		GroupBox groupBox4 = GroupBox2;
		size = new Size(441, 258);
		((Control)groupBox4).Size = size;
		((Control)GroupBox2).TabIndex = 4;
		GroupBox2.TabStop = false;
		GroupBox2.Text = "Shift Tables - Legacy Copy/Paste Export";
		((Control)Export_Grid).BackgroundImage = (Image)componentResourceManager.GetObject("Export_Grid.BackgroundImage");
		((Control)Export_Grid).BackgroundImageLayout = (ImageLayout)0;
		Export_Grid.Cell_Auto_W = 1;
		Export_Grid.Cell_CharMax = 3;
		Export_Grid.Cell_CPFormat = "##0.###";
		Export_Grid.Cell_FontCLR = Color.Black;
		Export_Grid.Cell_Format = "##0";
		Export_Grid.Cell_FSelCLR = Color.White;
		Export_Grid.Cell_H = 12;
		Export_Grid.Cell_HighCLR = Color.RoyalBlue;
		Export_Grid.Cell_HSelCLR = Color.DarkRed;
		Export_Grid.Cell_LabelFormat = "####0";
		Export_Grid.Cell_LowCLR = Color.White;
		Export_Grid.Cell_LSelCLR = Color.Red;
		Export_Grid.Cell_ShowChanges = 0;
		Export_Grid.Cell_W = 24;
		Export_Grid.Grid_AxisStatus = 0;
		Export_Grid.Grid_DataOffset = 0f;
		Export_Grid.Grid_DataScalar = 1f;
		Export_Grid.Grid_DataSCopyPaste = 1;
		Export_Grid.Grid_DataStatus = 1487;
		Export_Grid.Grid_FreezeDraw = 0;
		Export_Grid.Grid_GraphType = 1;
		Export_Grid.Grid_ReDraw = 0;
		Export_Grid.Grid_ShowLabels = 0;
		Export_Grid.Grid_Transpose = 0;
		Export_Grid.Grid_TransposeCopyPaste = 0;
		Export_Grid.Grid_VisibleName = "Export Table";
		Export_Grid.Grid_X = 17;
		Export_Grid.Grid_Y = 4;
		BCGridControl export_Grid = Export_Grid;
		location = new Point(16, 58);
		((Control)export_Grid).Location = location;
		((Control)Export_Grid).Name = "Export_Grid";
		BCGridControl export_Grid2 = Export_Grid;
		size = new Size(409, 49);
		((Control)export_Grid2).Size = size;
		((Control)Export_Grid).TabIndex = 6;
		Label7.AutoSize = true;
		Label label = Label7;
		location = new Point(13, 42);
		((Control)label).Location = location;
		((Control)Label7).Name = "Label7";
		Label label2 = Label7;
		size = new Size(65, 13);
		((Control)label2).Size = size;
		((Control)Label7).TabIndex = 5;
		Label7.Text = "Table Name";
		Button button = Button3;
		location = new Point(294, 19);
		((Control)button).Location = location;
		((Control)Button3).Name = "Button3";
		Button button2 = Button3;
		size = new Size(131, 21);
		((Control)button2).Size = size;
		((Control)Button3).TabIndex = 4;
		((ButtonBase)Button3).Text = "Copy Table";
		((ButtonBase)Button3).UseVisualStyleBackColor = true;
		Button button3 = Button2;
		location = new Point(143, 18);
		((Control)button3).Location = location;
		((Control)Button2).Name = "Button2";
		Button button4 = Button2;
		size = new Size(96, 21);
		((Control)button4).Size = size;
		((Control)Button2).TabIndex = 3;
		((ButtonBase)Button2).Text = "Next";
		((ButtonBase)Button2).UseVisualStyleBackColor = true;
		Label6.AutoSize = true;
		Label label3 = Label6;
		location = new Point(118, 21);
		((Control)label3).Location = location;
		((Control)Label6).Name = "Label6";
		Label label4 = Label6;
		size = new Size(19, 13);
		((Control)label4).Size = size;
		((Control)Label6).TabIndex = 2;
		Label6.Text = "<>";
		Button button5 = Button1;
		location = new Point(16, 18);
		((Control)button5).Location = location;
		((Control)Button1).Name = "Button1";
		Button button6 = Button1;
		size = new Size(96, 21);
		((Control)button6).Size = size;
		((Control)Button1).TabIndex = 1;
		((ButtonBase)Button1).Text = "Previous";
		((ButtonBase)Button1).UseVisualStyleBackColor = true;
		((Control)GroupBox1).Controls.Add((Control)(object)Label5);
		((Control)GroupBox1).Controls.Add((Control)(object)TextBox5);
		((Control)GroupBox1).Controls.Add((Control)(object)Label4);
		((Control)GroupBox1).Controls.Add((Control)(object)TextBox4);
		((Control)GroupBox1).Controls.Add((Control)(object)Label3);
		((Control)GroupBox1).Controls.Add((Control)(object)TextBox3);
		((Control)GroupBox1).Controls.Add((Control)(object)Label2);
		((Control)GroupBox1).Controls.Add((Control)(object)TextBox2);
		((Control)GroupBox1).Controls.Add((Control)(object)Label1);
		((Control)GroupBox1).Controls.Add((Control)(object)TextBox1);
		((Control)GroupBox1).Controls.Add((Control)(object)ComboBox2);
		GroupBox groupBox5 = GroupBox1;
		location = new Point(6, 16);
		((Control)groupBox5).Location = location;
		((Control)GroupBox1).Name = "GroupBox1";
		GroupBox groupBox6 = GroupBox1;
		size = new Size(193, 258);
		((Control)groupBox6).Size = size;
		((Control)GroupBox1).TabIndex = 3;
		GroupBox1.TabStop = false;
		GroupBox1.Text = "Speedometer Cal";
		Label5.AutoSize = true;
		Label label5 = Label5;
		location = new Point(6, 161);
		((Control)label5).Location = location;
		((Control)Label5).Name = "Label5";
		Label label6 = Label5;
		size = new Size(39, 13);
		((Control)label6).Size = size;
		((Control)Label5).TabIndex = 11;
		Label5.Text = "Label5";
		((TextBoxBase)TextBox5).BackColor = SystemColors.Window;
		TextBox textBox = TextBox5;
		location = new Point(102, 158);
		((Control)textBox).Location = location;
		((Control)TextBox5).Name = "TextBox5";
		((TextBoxBase)TextBox5).ReadOnly = true;
		TextBox textBox2 = TextBox5;
		size = new Size(85, 20);
		((Control)textBox2).Size = size;
		((Control)TextBox5).TabIndex = 10;
		Label4.AutoSize = true;
		Label label7 = Label4;
		location = new Point(6, 135);
		((Control)label7).Location = location;
		((Control)Label4).Name = "Label4";
		Label label8 = Label4;
		size = new Size(39, 13);
		((Control)label8).Size = size;
		((Control)Label4).TabIndex = 9;
		Label4.Text = "Label4";
		((TextBoxBase)TextBox4).BackColor = SystemColors.Window;
		TextBox textBox3 = TextBox4;
		location = new Point(102, 132);
		((Control)textBox3).Location = location;
		((Control)TextBox4).Name = "TextBox4";
		((TextBoxBase)TextBox4).ReadOnly = true;
		TextBox textBox4 = TextBox4;
		size = new Size(85, 20);
		((Control)textBox4).Size = size;
		((Control)TextBox4).TabIndex = 8;
		Label3.AutoSize = true;
		Label label9 = Label3;
		location = new Point(6, 109);
		((Control)label9).Location = location;
		((Control)Label3).Name = "Label3";
		Label label10 = Label3;
		size = new Size(39, 13);
		((Control)label10).Size = size;
		((Control)Label3).TabIndex = 7;
		Label3.Text = "Label3";
		((TextBoxBase)TextBox3).BackColor = SystemColors.Window;
		TextBox textBox5 = TextBox3;
		location = new Point(102, 106);
		((Control)textBox5).Location = location;
		((Control)TextBox3).Name = "TextBox3";
		((TextBoxBase)TextBox3).ReadOnly = true;
		TextBox textBox6 = TextBox3;
		size = new Size(85, 20);
		((Control)textBox6).Size = size;
		((Control)TextBox3).TabIndex = 6;
		Label2.AutoSize = true;
		Label label11 = Label2;
		location = new Point(6, 83);
		((Control)label11).Location = location;
		((Control)Label2).Name = "Label2";
		Label label12 = Label2;
		size = new Size(39, 13);
		((Control)label12).Size = size;
		((Control)Label2).TabIndex = 5;
		Label2.Text = "Label2";
		((TextBoxBase)TextBox2).BackColor = SystemColors.Window;
		TextBox textBox7 = TextBox2;
		location = new Point(102, 80);
		((Control)textBox7).Location = location;
		((Control)TextBox2).Name = "TextBox2";
		((TextBoxBase)TextBox2).ReadOnly = true;
		TextBox textBox8 = TextBox2;
		size = new Size(85, 20);
		((Control)textBox8).Size = size;
		((Control)TextBox2).TabIndex = 4;
		Label1.AutoSize = true;
		Label label13 = Label1;
		location = new Point(6, 57);
		((Control)label13).Location = location;
		((Control)Label1).Name = "Label1";
		Label label14 = Label1;
		size = new Size(39, 13);
		((Control)label14).Size = size;
		((Control)Label1).TabIndex = 3;
		Label1.Text = "Label1";
		((TextBoxBase)TextBox1).BackColor = SystemColors.Window;
		TextBox textBox9 = TextBox1;
		location = new Point(102, 54);
		((Control)textBox9).Location = location;
		((Control)TextBox1).Name = "TextBox1";
		((TextBoxBase)TextBox1).ReadOnly = true;
		TextBox textBox10 = TextBox1;
		size = new Size(85, 20);
		((Control)textBox10).Size = size;
		((Control)TextBox1).TabIndex = 3;
		ComboBox2.DropDownStyle = (ComboBoxStyle)2;
		((ListControl)ComboBox2).FormattingEnabled = true;
		ComboBox comboBox5 = ComboBox2;
		location = new Point(6, 19);
		((Control)comboBox5).Location = location;
		((Control)ComboBox2).Name = "ComboBox2";
		ComboBox comboBox6 = ComboBox2;
		size = new Size(181, 21);
		((Control)comboBox6).Size = size;
		((Control)ComboBox2).TabIndex = 1;
		((Control)GroupBox4).Controls.Add((Control)(object)CheckBox20);
		((Control)GroupBox4).Controls.Add((Control)(object)CheckBox18);
		((Control)GroupBox4).Controls.Add((Control)(object)GroupBox6);
		((Control)GroupBox4).Controls.Add((Control)(object)CheckBox19);
		((Control)GroupBox4).Controls.Add((Control)(object)ComboBox4);
		((Control)GroupBox4).Controls.Add((Control)(object)ComboBox3);
		((Control)GroupBox4).Controls.Add((Control)(object)CheckBox16);
		((Control)GroupBox4).Controls.Add((Control)(object)Gear);
		((Control)GroupBox4).Controls.Add((Control)(object)CheckBox15);
		((Control)GroupBox4).Controls.Add((Control)(object)Label8);
		((Control)GroupBox4).Controls.Add((Control)(object)CheckBox14);
		((Control)GroupBox4).Controls.Add((Control)(object)CheckBox13);
		((Control)GroupBox4).Controls.Add((Control)(object)CheckBox12);
		((Control)GroupBox4).Controls.Add((Control)(object)CheckBox11);
		((Control)GroupBox4).Controls.Add((Control)(object)CheckBox10);
		((Control)GroupBox4).Controls.Add((Control)(object)Button4);
		((Control)GroupBox4).Controls.Add((Control)(object)CheckBox9);
		((Control)GroupBox4).Controls.Add((Control)(object)CheckBox8);
		((Control)GroupBox4).Controls.Add((Control)(object)CheckBox7);
		((Control)GroupBox4).Controls.Add((Control)(object)CheckBox6);
		((Control)GroupBox4).Controls.Add((Control)(object)CheckBox5);
		((Control)GroupBox4).Controls.Add((Control)(object)CheckBox4);
		((Control)GroupBox4).Controls.Add((Control)(object)CheckBox3);
		((Control)GroupBox4).Controls.Add((Control)(object)CheckBox2);
		GroupBox groupBox7 = GroupBox4;
		location = new Point(15, 350);
		((Control)groupBox7).Location = location;
		((Control)GroupBox4).Name = "GroupBox4";
		GroupBox groupBox8 = GroupBox4;
		size = new Size(651, 209);
		((Control)groupBox8).Size = size;
		((Control)GroupBox4).TabIndex = 4;
		GroupBox4.TabStop = false;
		GroupBox4.Text = "HPT Template Export (.htt)";
		((Control)GroupBox6).Controls.Add((Control)(object)NDTire);
		((Control)GroupBox6).Controls.Add((Control)(object)CheckBox17);
		GroupBox groupBox9 = GroupBox6;
		location = new Point(451, 155);
		((Control)groupBox9).Location = location;
		((Control)GroupBox6).Name = "GroupBox6";
		GroupBox groupBox10 = GroupBox6;
		size = new Size(193, 45);
		((Control)groupBox10).Size = size;
		((Control)GroupBox6).TabIndex = 21;
		GroupBox6.TabStop = false;
		GroupBox6.Text = "Non-Driven Tire";
		NDTire.DecimalPlaces = 2;
		((Control)NDTire).Enabled = false;
		increment = (NDTire.Increment = new decimal(new int[4] { 1, 0, 0, 65536 }));
		NumericUpDown nDTire = NDTire;
		location = new Point(139, 19);
		((Control)nDTire).Location = location;
		increment = (NDTire.Maximum = new decimal(new int[4] { 150, 0, 0, 0 }));
		increment = (NDTire.Minimum = new decimal(new int[4] { 5, 0, 0, 0 }));
		((Control)NDTire).Name = "NDTire";
		NumericUpDown nDTire2 = NDTire;
		size = new Size(48, 20);
		((Control)nDTire2).Size = size;
		((Control)NDTire).TabIndex = 17;
		increment = (NDTire.Value = new decimal(new int[4] { 2491, 0, 0, 131072 }));
		((ButtonBase)CheckBox17).AutoSize = true;
		CheckBox checkBox13 = CheckBox17;
		location = new Point(16, 20);
		((Control)checkBox13).Location = location;
		((Control)CheckBox17).Name = "CheckBox17";
		CheckBox checkBox14 = CheckBox17;
		size = new Size(123, 17);
		((Control)checkBox14).Size = size;
		((Control)CheckBox17).TabIndex = 1;
		((ButtonBase)CheckBox17).Text = "Different from Driven";
		((ButtonBase)CheckBox17).UseVisualStyleBackColor = true;
		Label8.AutoSize = true;
		Label label15 = Label8;
		location = new Point(350, 189);
		((Control)label15).Location = location;
		((Control)Label8).Name = "Label8";
		Label label16 = Label8;
		size = new Size(32, 13);
		((Control)label16).Size = size;
		((Control)Label8).TabIndex = 15;
		Label8.Text = "Ratio";
		((ButtonBase)CheckBox14).AutoSize = true;
		CheckBox checkBox15 = CheckBox14;
		location = new Point(36, 134);
		((Control)checkBox15).Location = location;
		((Control)CheckBox14).Name = "CheckBox14";
		CheckBox checkBox16 = CheckBox14;
		size = new Size(153, 17);
		((Control)checkBox16).Size = size;
		((Control)CheckBox14).TabIndex = 13;
		((ButtonBase)CheckBox14).Text = "TUTD Enter in Lower Gear";
		((ButtonBase)CheckBox14).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox13).AutoSize = true;
		CheckBox checkBox17 = CheckBox13;
		location = new Point(218, 188);
		((Control)checkBox17).Location = location;
		((Control)CheckBox13).Name = "CheckBox13";
		CheckBox checkBox18 = CheckBox13;
		size = new Size(126, 17);
		((Control)checkBox18).Size = size;
		((Control)CheckBox13).TabIndex = 12;
		((ButtonBase)CheckBox13).Text = "Export to Low Range";
		((ButtonBase)CheckBox13).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox12).AutoSize = true;
		CheckBox checkBox19 = CheckBox12;
		location = new Point(36, 180);
		((Control)checkBox19).Location = location;
		((Control)CheckBox12).Name = "CheckBox12";
		CheckBox checkBox20 = CheckBox12;
		size = new Size(105, 17);
		((Control)checkBox20).Size = size;
		((Control)CheckBox12).TabIndex = 11;
		((ButtonBase)CheckBox12).Text = "Zero Saftey Shift";
		((ButtonBase)CheckBox12).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox11).AutoSize = true;
		CheckBox checkBox21 = CheckBox11;
		location = new Point(36, 65);
		((Control)checkBox21).Location = location;
		((Control)CheckBox11).Name = "CheckBox11";
		CheckBox checkBox22 = CheckBox11;
		size = new Size(110, 17);
		((Control)checkBox22).Size = size;
		((Control)CheckBox11).TabIndex = 10;
		((ButtonBase)CheckBox11).Text = "Zero Extra Tables";
		((ButtonBase)CheckBox11).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox10).AutoSize = true;
		CheckBox10.Checked = true;
		CheckBox10.CheckState = (CheckState)1;
		CheckBox checkBox23 = CheckBox10;
		location = new Point(13, 42);
		((Control)checkBox23).Location = location;
		((Control)CheckBox10).Name = "CheckBox10";
		CheckBox checkBox24 = CheckBox10;
		size = new Size(123, 17);
		((Control)checkBox24).Size = size;
		((Control)CheckBox10).TabIndex = 9;
		((ButtonBase)CheckBox10).Text = "Include Extra Tables";
		((ButtonBase)CheckBox10).UseVisualStyleBackColor = true;
		Button button7 = Button4;
		location = new Point(451, 17);
		((Control)button7).Location = location;
		((Control)Button4).Name = "Button4";
		Button button8 = Button4;
		size = new Size(175, 40);
		((Control)button8).Size = size;
		((Control)Button4).TabIndex = 8;
		((ButtonBase)Button4).Text = "Export";
		((ButtonBase)Button4).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox9).AutoSize = true;
		CheckBox9.Checked = true;
		CheckBox9.CheckState = (CheckState)1;
		CheckBox checkBox25 = CheckBox9;
		location = new Point(13, 157);
		((Control)checkBox25).Location = location;
		((Control)CheckBox9).Name = "CheckBox9";
		CheckBox checkBox26 = CheckBox9;
		size = new Size(118, 17);
		((Control)checkBox26).Size = size;
		((Control)CheckBox9).TabIndex = 7;
		((ButtonBase)CheckBox9).Text = "Include Saftey Shift";
		((ButtonBase)CheckBox9).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox8).AutoSize = true;
		CheckBox checkBox27 = CheckBox8;
		location = new Point(36, 111);
		((Control)checkBox27).Location = location;
		((Control)CheckBox8).Name = "CheckBox8";
		CheckBox checkBox28 = CheckBox8;
		size = new Size(160, 17);
		((Control)checkBox28).Size = size;
		((Control)CheckBox8).TabIndex = 6;
		((ButtonBase)CheckBox8).Text = "TUTD Auto Upshift @ WOT";
		((ButtonBase)CheckBox8).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox7).AutoSize = true;
		CheckBox7.Checked = true;
		CheckBox7.CheckState = (CheckState)1;
		CheckBox checkBox29 = CheckBox7;
		location = new Point(218, 165);
		((Control)checkBox29).Location = location;
		((Control)CheckBox7).Name = "CheckBox7";
		CheckBox checkBox30 = CheckBox7;
		size = new Size(88, 17);
		((Control)checkBox30).Size = size;
		((Control)CheckBox7).TabIndex = 5;
		((ButtonBase)CheckBox7).Text = "Export to Hot";
		((ButtonBase)CheckBox7).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox6).AutoSize = true;
		CheckBox6.Checked = true;
		CheckBox6.CheckState = (CheckState)1;
		CheckBox checkBox31 = CheckBox6;
		location = new Point(218, 92);
		((Control)checkBox31).Location = location;
		((Control)CheckBox6).Name = "CheckBox6";
		CheckBox checkBox32 = CheckBox6;
		size = new Size(155, 17);
		((Control)checkBox32).Size = size;
		((Control)CheckBox6).TabIndex = 4;
		((ButtonBase)CheckBox6).Text = "Export to Pattern B / Cruise";
		((ButtonBase)CheckBox6).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox5).AutoSize = true;
		CheckBox5.Checked = true;
		CheckBox5.CheckState = (CheckState)1;
		CheckBox checkBox33 = CheckBox5;
		location = new Point(218, 42);
		((Control)checkBox33).Location = location;
		((Control)CheckBox5).Name = "CheckBox5";
		CheckBox checkBox34 = CheckBox5;
		size = new Size(186, 17);
		((Control)checkBox34).Size = size;
		((Control)CheckBox5).TabIndex = 3;
		((ButtonBase)CheckBox5).Text = "Export to Pattern A / Performance";
		((ButtonBase)CheckBox5).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox4).AutoSize = true;
		CheckBox4.Checked = true;
		CheckBox4.CheckState = (CheckState)1;
		CheckBox checkBox35 = CheckBox4;
		location = new Point(218, 19);
		((Control)checkBox35).Location = location;
		((Control)CheckBox4).Name = "CheckBox4";
		CheckBox checkBox36 = CheckBox4;
		size = new Size(104, 17);
		((Control)checkBox36).Size = size;
		((Control)CheckBox4).TabIndex = 2;
		((ButtonBase)CheckBox4).Text = "Export to Normal";
		((ButtonBase)CheckBox4).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox3).AutoSize = true;
		CheckBox3.Checked = true;
		CheckBox3.CheckState = (CheckState)1;
		CheckBox checkBox37 = CheckBox3;
		location = new Point(13, 88);
		((Control)checkBox37).Location = location;
		((Control)CheckBox3).Name = "CheckBox3";
		CheckBox checkBox38 = CheckBox3;
		size = new Size(94, 17);
		((Control)checkBox38).Size = size;
		((Control)CheckBox3).TabIndex = 1;
		((ButtonBase)CheckBox3).Text = "Include TUTD";
		((ButtonBase)CheckBox3).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox2).AutoSize = true;
		CheckBox2.Checked = true;
		CheckBox2.CheckState = (CheckState)1;
		CheckBox checkBox39 = CheckBox2;
		location = new Point(13, 19);
		((Control)checkBox39).Location = location;
		((Control)CheckBox2).Name = "CheckBox2";
		CheckBox checkBox40 = CheckBox2;
		size = new Size(145, 17);
		((Control)checkBox40).Size = size;
		((Control)CheckBox2).TabIndex = 0;
		((ButtonBase)CheckBox2).Text = "Include Speedometer Cal";
		((ButtonBase)CheckBox2).UseVisualStyleBackColor = true;
		((FileDialog)SaveFileDialog1).DefaultExt = "htt";
		((FileDialog)SaveFileDialog1).Filter = "HP Tuners Template Files (*.htt)|*.htt";
		((FileDialog)SaveFileDialog1).InitialDirectory = ".";
		((FileDialog)SaveFileDialog1).Title = "Export Template File";
		((Control)GroupBox5).Controls.Add((Control)(object)CheckBox21);
		((Control)GroupBox5).Controls.Add((Control)(object)CheckBox1);
		((Control)GroupBox5).Controls.Add((Control)(object)ComboBox1);
		GroupBox groupBox11 = GroupBox5;
		location = new Point(13, 8);
		((Control)groupBox11).Location = location;
		((Control)GroupBox5).Name = "GroupBox5";
		GroupBox groupBox12 = GroupBox5;
		size = new Size(652, 48);
		((Control)groupBox12).Size = size;
		((Control)GroupBox5).TabIndex = 5;
		GroupBox5.TabStop = false;
		GroupBox5.Text = "Export Type";
		((ButtonBase)CheckBox1).AutoSize = true;
		CheckBox checkBox41 = CheckBox1;
		location = new Point(183, 21);
		((Control)checkBox41).Location = location;
		((Control)CheckBox1).Name = "CheckBox1";
		CheckBox checkBox42 = CheckBox1;
		size = new Size(99, 17);
		((Control)checkBox42).Size = size;
		((Control)CheckBox1).TabIndex = 8;
		((ButtonBase)CheckBox1).Text = "2 Column WOT";
		((ButtonBase)CheckBox1).UseVisualStyleBackColor = true;
		ComboBox1.DropDownStyle = (ComboBoxStyle)2;
		((ListControl)ComboBox1).FormattingEnabled = true;
		ComboBox comboBox7 = ComboBox1;
		location = new Point(6, 19);
		((Control)comboBox7).Location = location;
		((Control)ComboBox1).Name = "ComboBox1";
		ComboBox comboBox8 = ComboBox1;
		size = new Size(163, 21);
		((Control)comboBox8).Size = size;
		((Control)ComboBox1).TabIndex = 1;
		SizeF autoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleDimensions = autoScaleDimensions;
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		size = new Size(678, 574);
		((Form)this).ClientSize = size;
		((Control)this).Controls.Add((Control)(object)GroupBox5);
		((Control)this).Controls.Add((Control)(object)GroupBox4);
		((Control)this).Controls.Add((Control)(object)GroupBox3);
		((Control)this).DoubleBuffered = true;
		((Form)this).FormBorderStyle = (FormBorderStyle)1;
		((Form)this).Icon = (Icon)componentResourceManager.GetObject("$this.Icon");
		((Form)this).MaximizeBox = false;
		((Control)this).Name = "Export_Form";
		((Form)this).StartPosition = (FormStartPosition)1;
		((Form)this).Text = "Export Data";
		((ISupportInitialize)Gear).EndInit();
		((Control)GroupBox3).ResumeLayout(false);
		((Control)GroupBox2).ResumeLayout(false);
		((Control)GroupBox2).PerformLayout();
		((Control)GroupBox1).ResumeLayout(false);
		((Control)GroupBox1).PerformLayout();
		((Control)GroupBox4).ResumeLayout(false);
		((Control)GroupBox4).PerformLayout();
		((Control)GroupBox6).ResumeLayout(false);
		((Control)GroupBox6).PerformLayout();
		((ISupportInitialize)NDTire).EndInit();
		((Control)GroupBox5).ResumeLayout(false);
		((Control)GroupBox5).PerformLayout();
		((Control)this).ResumeLayout(false);
	}

	private void Form_Closing(object sender, CancelEventArgs e)
	{
		e.Cancel = true;
		((Control)this).Hide();
	}

	private void ComboBox2_SelectedIndexChanged(object sender, EventArgs e)
	{
		int[] array = VSS_For(ComboBox1.SelectedIndex);
		if (array.Length > 0 && !In_Set(ComboBox2.SelectedIndex, array))
		{
			int num = First_Valid(array, ComboBox2.Items.Count);
			if (num >= 0)
			{
				ComboBox2.SelectedIndex = num;
				return;
			}
		}
		Update_VSS();
		Update_Export();
	}

	private void ComboBox1_SelectedIndexChanged(object sender, EventArgs e)
	{
		if (ExportAllowed.Length > 0 && !In_Set(ComboBox1.SelectedIndex, ExportAllowed))
		{
			int num = First_Valid(ExportAllowed, ComboBox1.Items.Count);
			if (num >= 0)
			{
				ComboBox1.SelectedIndex = num;
				return;
			}
		}
		EMD = 1;
		if ((ComboBox1.SelectedIndex == 2) | (ComboBox1.SelectedIndex == 3))
		{
			((Control)CheckBox1).Visible = true;
		}
		else
		{
			((Control)CheckBox1).Visible = false;
			CheckBox1.Checked = false;
		}
		if (ComboBox1.SelectedIndex == 1)
		{
			((Control)Button4).Enabled = true;
			((Control)CheckBox2).Enabled = true;
			((Control)CheckBox10).Enabled = true;
			((Control)CheckBox11).Enabled = true;
			((Control)CheckBox3).Enabled = false;
			((Control)CheckBox8).Enabled = false;
			((Control)CheckBox14).Enabled = false;
			((Control)CheckBox9).Enabled = false;
			((Control)CheckBox12).Enabled = false;
			((Control)CheckBox4).Enabled = true;
			((Control)CheckBox5).Enabled = true;
			((Control)ComboBox3).Enabled = true;
			((Control)CheckBox6).Enabled = true;
			((Control)ComboBox4).Enabled = true;
			((Control)CheckBox18).Enabled = false;
			((Control)CheckBox7).Enabled = true;
			((Control)CheckBox13).Enabled = true;
			((Control)Gear).Enabled = true;
			((Control)CheckBox15).Enabled = false;
			((Control)CheckBox16).Enabled = false;
			((Control)CheckBox19).Enabled = true;
			((Control)CheckBox20).Enabled = true;
			((Control)GroupBox6).Enabled = false;
			((Control)MyProject.Forms.TCC_Form.GroupBox3).Enabled = true;
		}
		else if (ComboBox1.SelectedIndex == 2)
		{
			((Control)Button4).Enabled = true;
			((Control)CheckBox2).Enabled = true;
			((Control)CheckBox10).Enabled = true;
			((Control)CheckBox11).Enabled = true;
			((Control)CheckBox3).Enabled = true;
			((Control)CheckBox8).Enabled = true;
			((Control)CheckBox14).Enabled = false;
			((Control)CheckBox9).Enabled = true;
			((Control)CheckBox12).Enabled = true;
			((Control)CheckBox4).Enabled = true;
			((Control)CheckBox5).Enabled = true;
			((Control)ComboBox3).Enabled = true;
			((Control)CheckBox6).Enabled = true;
			((Control)ComboBox4).Enabled = true;
			((Control)CheckBox18).Enabled = false;
			((Control)CheckBox7).Enabled = true;
			((Control)CheckBox13).Enabled = true;
			((Control)Gear).Enabled = true;
			((Control)CheckBox15).Enabled = false;
			((Control)CheckBox16).Enabled = false;
			((Control)CheckBox19).Enabled = true;
			((Control)CheckBox20).Enabled = true;
			((Control)GroupBox6).Enabled = true;
			((Control)MyProject.Forms.TCC_Form.GroupBox3).Enabled = true;
		}
		else if ((ComboBox1.SelectedIndex == 3) | (ComboBox1.SelectedIndex == 4))
		{
			((Control)Button4).Enabled = true;
			((Control)CheckBox2).Enabled = true;
			((Control)CheckBox10).Enabled = true;
			((Control)CheckBox11).Enabled = true;
			((Control)CheckBox3).Enabled = true;
			((Control)CheckBox8).Enabled = true;
			((Control)CheckBox14).Enabled = true;
			((Control)CheckBox9).Enabled = true;
			((Control)CheckBox12).Enabled = true;
			((Control)CheckBox4).Enabled = true;
			((Control)CheckBox5).Enabled = true;
			((Control)ComboBox3).Enabled = true;
			((Control)CheckBox6).Enabled = true;
			((Control)ComboBox4).Enabled = true;
			((Control)CheckBox18).Enabled = false;
			((Control)CheckBox7).Enabled = true;
			((Control)CheckBox13).Enabled = true;
			((Control)Gear).Enabled = true;
			((Control)CheckBox15).Enabled = true;
			((Control)CheckBox16).Enabled = true;
			((Control)CheckBox19).Enabled = false;
			((Control)CheckBox20).Enabled = true;
			((Control)GroupBox6).Enabled = true;
			((Control)MyProject.Forms.TCC_Form.GroupBox3).Enabled = false;
		}
		else if (ComboBox1.SelectedIndex == 5)
		{
			((Control)Button4).Enabled = true;
			((Control)CheckBox2).Enabled = true;
			((Control)CheckBox10).Enabled = true;
			((Control)CheckBox11).Enabled = true;
			((Control)CheckBox3).Enabled = true;
			((Control)CheckBox8).Enabled = true;
			((Control)CheckBox14).Enabled = false;
			((Control)CheckBox9).Enabled = false;
			((Control)CheckBox12).Enabled = false;
			((Control)CheckBox4).Enabled = true;
			((Control)CheckBox5).Enabled = true;
			((Control)ComboBox3).Enabled = true;
			((Control)CheckBox6).Enabled = true;
			((Control)ComboBox4).Enabled = true;
			((Control)CheckBox18).Enabled = false;
			((Control)CheckBox7).Enabled = true;
			((Control)CheckBox13).Enabled = true;
			((Control)Gear).Enabled = true;
			((Control)CheckBox15).Enabled = true;
			((Control)CheckBox16).Enabled = true;
			((Control)CheckBox19).Enabled = false;
			((Control)CheckBox20).Enabled = true;
			((Control)GroupBox6).Enabled = true;
			((Control)MyProject.Forms.TCC_Form.GroupBox3).Enabled = false;
		}
		else if ((ComboBox1.SelectedIndex == 6) | (ComboBox1.SelectedIndex == 7))
		{
			((Control)Button4).Enabled = true;
			((Control)CheckBox2).Enabled = true;
			((Control)CheckBox10).Enabled = true;
			((Control)CheckBox11).Enabled = true;
			((Control)CheckBox3).Enabled = true;
			((Control)CheckBox8).Enabled = true;
			((Control)CheckBox14).Enabled = false;
			((Control)CheckBox9).Enabled = false;
			((Control)CheckBox12).Enabled = false;
			((Control)CheckBox4).Enabled = true;
			((Control)CheckBox5).Enabled = true;
			((Control)ComboBox3).Enabled = true;
			((Control)CheckBox6).Enabled = true;
			((Control)ComboBox4).Enabled = true;
			((Control)CheckBox18).Enabled = true;
			((Control)CheckBox7).Enabled = true;
			((Control)CheckBox13).Enabled = true;
			((Control)Gear).Enabled = true;
			((Control)CheckBox15).Enabled = true;
			((Control)CheckBox16).Enabled = true;
			((Control)CheckBox19).Enabled = false;
			((Control)CheckBox20).Enabled = true;
			((Control)GroupBox6).Enabled = true;
			((Control)MyProject.Forms.TCC_Form.GroupBox3).Enabled = false;
		}
		else
		{
			((Control)Button4).Enabled = false;
			((Control)CheckBox2).Enabled = false;
			((Control)CheckBox10).Enabled = false;
			((Control)CheckBox11).Enabled = false;
			((Control)CheckBox3).Enabled = false;
			((Control)CheckBox8).Enabled = false;
			((Control)CheckBox14).Enabled = false;
			((Control)CheckBox9).Enabled = false;
			((Control)CheckBox12).Enabled = false;
			((Control)CheckBox4).Enabled = false;
			((Control)CheckBox5).Enabled = false;
			((Control)ComboBox3).Enabled = false;
			((Control)CheckBox6).Enabled = false;
			((Control)ComboBox4).Enabled = false;
			((Control)CheckBox18).Enabled = false;
			((Control)CheckBox7).Enabled = false;
			((Control)CheckBox13).Enabled = false;
			((Control)Gear).Enabled = false;
			((Control)CheckBox15).Enabled = false;
			((Control)CheckBox16).Enabled = false;
			((Control)CheckBox19).Enabled = false;
			((Control)CheckBox20).Enabled = false;
			((Control)GroupBox6).Enabled = false;
			((Control)MyProject.Forms.TCC_Form.GroupBox3).Enabled = false;
		}
		((Control)ComboBox2).Invalidate();
		ComboBox2_SelectedIndexChanged(null, null);
	}

	public void Set_Export_Options(int[] allowed)
	{
		if (allowed == null)
		{
			allowed = new int[0];
		}
		ExportAllowed = allowed;
		((Control)ComboBox1).Invalidate();
		ComboBox1_SelectedIndexChanged(null, null);
	}

	private int[] VSS_For(int exportIdx)
	{
		if ((exportIdx >= 0) & (exportIdx < VSSOptions.Length))
		{
			return VSSOptions[exportIdx];
		}
		return new int[0];
	}

	private bool In_Set(int v, int[] opts)
	{
		checked
		{
			int num = opts.Length - 1;
			for (int i = 0; i <= num; i++)
			{
				if (opts[i] == v)
				{
					return true;
				}
			}
			return false;
		}
	}

	private int First_Valid(int[] opts, int count)
	{
		checked
		{
			int num = opts.Length - 1;
			for (int i = 0; i <= num; i++)
			{
				if ((opts[i] >= 0) & (opts[i] < count))
				{
					return opts[i];
				}
			}
			return -1;
		}
	}

	private void ComboBox1_DrawItem(object sender, DrawItemEventArgs e)
	{
		Draw_Combo_Item(ComboBox1, e, ExportAllowed);
	}

	private void ComboBox2_DrawItem(object sender, DrawItemEventArgs e)
	{
		Draw_Combo_Item(ComboBox2, e, VSS_For(ComboBox1.SelectedIndex));
	}

	private void Draw_Combo_Item(ComboBox cb, DrawItemEventArgs e, int[] opts)
	{
		if (e.Index >= 0)
		{
			e.DrawBackground();
			Color color = ((opts.Length != 0 && !In_Set(e.Index, opts)) ? SystemColors.GrayText : e.ForeColor);
			TextRenderer.DrawText((IDeviceContext)(object)e.Graphics, cb.Items[e.Index].ToString(), e.Font, e.Bounds, color, (TextFormatFlags)4);
			e.DrawFocusRectangle();
		}
	}

	private void CheckBox1_CheckedChanged(object sender, EventArgs e)
	{
		Update_Export();
	}

	private void CheckBox8_CheckedChanged(object sender, EventArgs e)
	{
		Update_Export();
	}

	private void CheckBox11_CheckedChanged(object sender, EventArgs e)
	{
		Update_Export();
	}

	private void CheckBox12_CheckedChanged(object sender, EventArgs e)
	{
		Update_Export();
	}

	public void Update_VSS()
	{
		float num = (float)(Convert.ToDouble(MyProject.Forms.Main_Form.Tire.Value) * 3.141592);
		float num2 = (float)(Convert.ToDouble(NDTire.Value) * 3.141592);
		float num3 = 63360f / num;
		float num4 = num3 * Convert.ToSingle(MyProject.Forms.Main_Form.Gear.Value);
		if (ComboBox1.SelectedIndex == 0)
		{
			((Control)ComboBox2).Visible = false;
			((Control)ComboBox2).Enabled = false;
			((Control)Label1).Visible = false;
			Label1.Text = "";
			((Control)TextBox1).Visible = false;
			TextBox1.Text = "";
			((Control)Label2).Visible = false;
			Label2.Text = "";
			((Control)TextBox2).Visible = false;
			TextBox2.Text = "";
			((Control)Label3).Visible = false;
			Label3.Text = "";
			((Control)TextBox3).Visible = false;
			TextBox3.Text = "";
			((Control)Label4).Visible = false;
			Label4.Text = "";
			((Control)TextBox4).Visible = false;
			TextBox4.Text = "";
			((Control)Label5).Visible = false;
			Label5.Text = "";
			((Control)TextBox5).Visible = false;
			TextBox5.Text = "";
			return;
		}
		((Control)ComboBox2).Visible = true;
		((Control)ComboBox2).Enabled = true;
		if ((ComboBox2.SelectedIndex == 0) | (ComboBox2.SelectedIndex == 1) | (ComboBox2.SelectedIndex == 2) | (ComboBox2.SelectedIndex == 3))
		{
			double num5 = ((!((ComboBox2.SelectedIndex == 1) | (ComboBox2.SelectedIndex == 3))) ? 1.0 : Convert.ToDouble(MyProject.Forms.Main_Form.Gear.Value));
			((Control)Label1).Visible = true;
			((Control)TextBox1).Visible = true;
			if (!MyProject.Forms.Main_Form.Metric.Checked)
			{
				Label1.Text = "VSS Pulses/mi";
				TextBox1.Text = Strings.Format((object)((double)num4 * (Convert.ToDouble(MyProject.Forms.Main_Form.VSS.Value) / num5)), "#####.###");
			}
			else
			{
				Label1.Text = "VSS Pulses/km";
				TextBox1.Text = Strings.Format((object)((double)num4 / 1.609 * (Convert.ToDouble(MyProject.Forms.Main_Form.VSS.Value) / num5)), "#####.###");
			}
			((Control)Label2).Visible = true;
			Label2.Text = "VSS Count";
			((Control)TextBox2).Visible = true;
			TextBox2.Text = Strings.Format((object)(Convert.ToDouble(MyProject.Forms.Main_Form.VSS.Value) / num5), "#####.###");
			if ((ComboBox2.SelectedIndex == 0) | (ComboBox2.SelectedIndex == 1))
			{
				((Control)Label3).Visible = true;
				Label3.Text = "Tire / Gear";
				((Control)TextBox3).Visible = true;
				TextBox3.Text = Strings.Format((object)decimal.Divide(MyProject.Forms.Main_Form.Tire.Value, MyProject.Forms.Main_Form.Gear.Value), "#####.####");
			}
			else
			{
				((Control)Label3).Visible = true;
				Label3.Text = "Gear Ratio";
				((Control)TextBox3).Visible = true;
				TextBox3.Text = Strings.Format((object)MyProject.Forms.Main_Form.Gear.Value, "#####.00");
			}
			((Control)Label4).Visible = true;
			((Control)TextBox4).Visible = true;
			if (!MyProject.Forms.Main_Form.Metric.Checked)
			{
				Label4.Text = "Trans Rev/mi";
				TextBox4.Text = Strings.Format((object)num4, "#####.###");
			}
			else
			{
				Label4.Text = "Trans Rev/km";
				TextBox4.Text = Strings.Format((object)((double)num4 / 1.609), "#####.###");
			}
			((Control)Label5).Visible = false;
			Label5.Text = "";
			((Control)TextBox5).Visible = false;
			TextBox5.Text = "";
		}
		else if (ComboBox2.SelectedIndex >= 4)
		{
			((Control)Label1).Visible = true;
			Label1.Text = "VSS Count";
			((Control)TextBox1).Visible = true;
			TextBox1.Text = Strings.Format((object)MyProject.Forms.Main_Form.VSS.Value, "#####.###");
			((Control)Label2).Visible = true;
			((Control)TextBox2).Visible = true;
			if (!MyProject.Forms.Main_Form.Metric.Checked)
			{
				Label2.Text = "Tire Rev/mi";
				TextBox2.Text = Strings.Format((object)num3, "#####.###");
			}
			else
			{
				Label2.Text = "Tire Rev/km";
				TextBox2.Text = Strings.Format((object)((double)num3 / 1.609), "#####.###");
			}
			((Control)Label3).Visible = true;
			Label3.Text = "Gear Ratio";
			((Control)TextBox3).Visible = true;
			if (ComboBox2.SelectedIndex == 5)
			{
				TextBox3.Text = Strings.Format((object)1.0, "#####.00");
			}
			else
			{
				TextBox3.Text = Strings.Format((object)MyProject.Forms.Main_Form.Gear.Value, "#####.00");
			}
			((Control)Label4).Visible = true;
			((Control)TextBox4).Visible = true;
			if (!MyProject.Forms.Main_Form.Metric.Checked)
			{
				Label4.Text = "Tire Circ. in";
				TextBox4.Text = Strings.Format((object)num, "#####.###");
			}
			else
			{
				Label4.Text = "Tire Circ. mm";
				TextBox4.Text = Strings.Format((object)((double)num * 25.4), "#####.###");
			}
			((Control)Label5).Visible = true;
			((Control)TextBox5).Visible = true;
			if (!MyProject.Forms.Main_Form.Metric.Checked)
			{
				Label5.Text = "ND Tire Circ. in";
				TextBox5.Text = Strings.Format((object)num2, "#####.###");
			}
			else
			{
				Label5.Text = "ND Tire Circ. mm";
				TextBox5.Text = Strings.Format((object)num2, "#####.###");
			}
		}
	}

	public void Update_Export()
	{
		if (ComboBox1.SelectedIndex == 0)
		{
			EMD = 1;
			((Control)Export_Grid).Visible = false;
			Label7.Text = "";
		}
		FileStream TempFile = default(FileStream);
		if (ComboBox1.SelectedIndex == 1)
		{
			((Control)Export_Grid).Visible = true;
			EMD_MAX = 12;
			if (EMD < 1)
			{
				EMD = 1;
			}
			if ((uint)EMD > (uint)EMD_MAX)
			{
				EMD = EMD_MAX;
			}
			if (EMD == 1)
			{
				Gen_Table(1, 0, 0, ref TempFile);
			}
			if (EMD == 2)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(3, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(2, 0, 0, ref TempFile);
				}
			}
			if (EMD == 3)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(5, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(4, 0, 0, ref TempFile);
				}
			}
			if (EMD == 4)
			{
				Gen_Table(6, 0, 0, ref TempFile);
			}
			if (EMD == 5)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(8, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(7, 0, 0, ref TempFile);
				}
			}
			if (EMD == 6)
			{
				Gen_Table(28, 0, 0, ref TempFile);
			}
			if (EMD == 7)
			{
				Gen_Table(29, 0, 0, ref TempFile);
			}
			if (EMD == 8)
			{
				Gen_Table(30, 0, 1, ref TempFile);
			}
			if (EMD == 9)
			{
				Gen_Table(30, 0, 2, ref TempFile);
			}
			if (EMD == 10)
			{
				Gen_Table(31, 0, 1, ref TempFile);
			}
			if (EMD == 11)
			{
				Gen_Table(31, 0, 2, ref TempFile);
			}
			if (EMD == 12)
			{
				Gen_Table(32, 0, 0, ref TempFile);
			}
		}
		if (ComboBox1.SelectedIndex == 2)
		{
			((Control)Export_Grid).Visible = true;
			EMD_MAX = 15;
			if (EMD < 1)
			{
				EMD = 1;
			}
			if ((uint)EMD > (uint)EMD_MAX)
			{
				EMD = EMD_MAX;
			}
			if (EMD == 1)
			{
				Gen_Table(1, 0, 0, ref TempFile);
			}
			if (EMD == 2)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(3, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(2, 0, 0, ref TempFile);
				}
			}
			if (EMD == 3)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(5, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(4, 0, 0, ref TempFile);
				}
			}
			if (EMD == 4)
			{
				Gen_Table(6, 0, 0, ref TempFile);
			}
			if (EMD == 5)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(8, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(7, 0, 0, ref TempFile);
				}
			}
			if (EMD == 6)
			{
				Gen_Table(33, 0, 0, ref TempFile);
			}
			if (EMD == 7)
			{
				Gen_Table(30, 0, 0, ref TempFile);
			}
			if (EMD == 8)
			{
				Gen_Table(34, 0, 0, ref TempFile);
			}
			if (EMD == 9)
			{
				Gen_Table(35, 0, 0, ref TempFile);
			}
			if (EMD == 10)
			{
				Gen_Table(37, 0, 0, ref TempFile);
			}
			if (EMD == 11)
			{
				Gen_Table(38, 0, 1, ref TempFile);
			}
			if (EMD == 12)
			{
				Gen_Table(52, 0, 1, ref TempFile);
			}
			if (EMD == 13)
			{
				Gen_Table(52, 0, 2, ref TempFile);
			}
			if (EMD == 14)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(54, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(53, 0, 0, ref TempFile);
				}
			}
			if (EMD == 15)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(62, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(61, 0, 0, ref TempFile);
				}
			}
		}
		if (ComboBox1.SelectedIndex == 3)
		{
			((Control)Export_Grid).Visible = true;
			EMD_MAX = 41;
			if (EMD < 1)
			{
				EMD = 1;
			}
			if ((uint)EMD > (uint)EMD_MAX)
			{
				EMD = EMD_MAX;
			}
			if (EMD == 1)
			{
				Gen_Table(1, 0, 0, ref TempFile);
			}
			if (EMD == 2)
			{
				Gen_Table(9, 0, 0, ref TempFile);
			}
			if (EMD == 3)
			{
				Gen_Table(10, 0, 0, ref TempFile);
			}
			if (EMD == 4)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(3, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(2, 0, 0, ref TempFile);
				}
			}
			if (EMD == 5)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(12, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(11, 0, 0, ref TempFile);
				}
			}
			if (EMD == 6)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(14, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(13, 0, 0, ref TempFile);
				}
			}
			if (EMD == 7)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(5, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(4, 0, 0, ref TempFile);
				}
			}
			if (EMD == 8)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(16, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(15, 0, 0, ref TempFile);
				}
			}
			if (EMD == 9)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(18, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(17, 0, 0, ref TempFile);
				}
			}
			if (EMD == 10)
			{
				Gen_Table(25, 0, 0, ref TempFile);
			}
			if (EMD == 11)
			{
				Gen_Table(19, 0, 0, ref TempFile);
			}
			if (EMD == 12)
			{
				Gen_Table(20, 0, 0, ref TempFile);
			}
			if (EMD == 13)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(27, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(26, 0, 0, ref TempFile);
				}
			}
			if (EMD == 14)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(22, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(21, 0, 0, ref TempFile);
				}
			}
			if (EMD == 15)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(24, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(23, 0, 0, ref TempFile);
				}
			}
			if (EMD == 16)
			{
				Gen_Table(33, 0, 0, ref TempFile);
			}
			if (EMD == 17)
			{
				Gen_Table(30, 0, 0, ref TempFile);
			}
			if (EMD == 18)
			{
				Gen_Table(36, 0, 0, ref TempFile);
			}
			if (EMD == 19)
			{
				Gen_Table(37, 0, 0, ref TempFile);
			}
			if (EMD == 20)
			{
				Gen_Table(38, 0, 0, ref TempFile);
			}
			if (EMD == 21)
			{
				Gen_Table(38, 0, 2, ref TempFile);
			}
			if (EMD == 22)
			{
				Gen_Table(39, 0, 0, ref TempFile);
			}
			if (EMD == 23)
			{
				Gen_Table(40, 0, 0, ref TempFile);
			}
			if (EMD == 24)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(42, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(41, 0, 0, ref TempFile);
				}
			}
			if (EMD == 25)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(44, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(43, 0, 0, ref TempFile);
				}
			}
			if (EMD == 26)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(46, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(45, 0, 0, ref TempFile);
				}
			}
			if (EMD == 27)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(48, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(47, 0, 0, ref TempFile);
				}
			}
			if (EMD == 28)
			{
				Gen_Table(49, 0, 1, ref TempFile);
			}
			if (EMD == 29)
			{
				Gen_Table(49, 0, 2, ref TempFile);
			}
			if (EMD == 30)
			{
				Gen_Table(50, 0, 0, ref TempFile);
			}
			if (EMD == 31)
			{
				Gen_Table(51, 0, 0, ref TempFile);
			}
			if (EMD == 32)
			{
				Gen_Table(50, 0, 1, ref TempFile);
			}
			if (EMD == 33)
			{
				Gen_Table(50, 0, 2, ref TempFile);
			}
			if (EMD == 34)
			{
				Gen_Table(51, 0, 1, ref TempFile);
			}
			if (EMD == 35)
			{
				Gen_Table(51, 0, 2, ref TempFile);
			}
			if (EMD == 36)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(54, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(53, 0, 0, ref TempFile);
				}
			}
			if (EMD == 37)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(62, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(61, 0, 0, ref TempFile);
				}
			}
			if (EMD == 38)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(56, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(55, 0, 0, ref TempFile);
				}
			}
			if (EMD == 39)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(58, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(57, 0, 0, ref TempFile);
				}
			}
			if (EMD == 40)
			{
				Gen_Table(59, 0, 0, ref TempFile);
			}
			if (EMD == 41)
			{
				Gen_Table(60, 0, 0, ref TempFile);
			}
		}
		if (ComboBox1.SelectedIndex == 4)
		{
			((Control)Export_Grid).Visible = true;
			EMD_MAX = 47;
			if (EMD < 1)
			{
				EMD = 1;
			}
			if ((uint)EMD > (uint)EMD_MAX)
			{
				EMD = EMD_MAX;
			}
			if (EMD == 1)
			{
				Gen_Table(1, 0, 1, ref TempFile);
			}
			if (EMD == 2)
			{
				Gen_Table(1, 0, 2, ref TempFile);
			}
			if (EMD == 3)
			{
				Gen_Table(9, 0, 1, ref TempFile);
			}
			if (EMD == 4)
			{
				Gen_Table(9, 0, 2, ref TempFile);
			}
			if (EMD == 5)
			{
				Gen_Table(10, 0, 1, ref TempFile);
			}
			if (EMD == 6)
			{
				Gen_Table(10, 0, 2, ref TempFile);
			}
			if (EMD == 7)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(3, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(2, 0, 0, ref TempFile);
				}
			}
			if (EMD == 8)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(12, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(11, 0, 0, ref TempFile);
				}
			}
			if (EMD == 9)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(14, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(13, 0, 0, ref TempFile);
				}
			}
			if (EMD == 10)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(5, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(4, 0, 0, ref TempFile);
				}
			}
			if (EMD == 11)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(16, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(15, 0, 0, ref TempFile);
				}
			}
			if (EMD == 12)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(18, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(17, 0, 0, ref TempFile);
				}
			}
			if (EMD == 13)
			{
				Gen_Table(25, 0, 1, ref TempFile);
			}
			if (EMD == 14)
			{
				Gen_Table(25, 0, 2, ref TempFile);
			}
			if (EMD == 15)
			{
				Gen_Table(19, 0, 1, ref TempFile);
			}
			if (EMD == 16)
			{
				Gen_Table(19, 0, 2, ref TempFile);
			}
			if (EMD == 17)
			{
				Gen_Table(20, 0, 0, ref TempFile);
			}
			if (EMD == 18)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(27, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(26, 0, 0, ref TempFile);
				}
			}
			if (EMD == 19)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(22, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(21, 0, 0, ref TempFile);
				}
			}
			if (EMD == 20)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(24, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(23, 0, 0, ref TempFile);
				}
			}
			if (EMD == 21)
			{
				Gen_Table(33, 0, 0, ref TempFile);
			}
			if (EMD == 22)
			{
				Gen_Table(30, 0, 0, ref TempFile);
			}
			if (EMD == 23)
			{
				Gen_Table(36, 0, 0, ref TempFile);
			}
			if (EMD == 24)
			{
				Gen_Table(37, 0, 0, ref TempFile);
			}
			if (EMD == 25)
			{
				Gen_Table(38, 0, 1, ref TempFile);
			}
			if (EMD == 26)
			{
				Gen_Table(38, 0, 2, ref TempFile);
			}
			if (EMD == 27)
			{
				Gen_Table(39, 0, 1, ref TempFile);
			}
			if (EMD == 28)
			{
				Gen_Table(39, 0, 2, ref TempFile);
			}
			if (EMD == 29)
			{
				Gen_Table(40, 0, 1, ref TempFile);
			}
			if (EMD == 30)
			{
				Gen_Table(40, 0, 2, ref TempFile);
			}
			if (EMD == 31)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(42, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(41, 0, 0, ref TempFile);
				}
			}
			if (EMD == 32)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(44, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(43, 0, 0, ref TempFile);
				}
			}
			if (EMD == 33)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(46, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(45, 0, 0, ref TempFile);
				}
			}
			if (EMD == 34)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(48, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(47, 0, 0, ref TempFile);
				}
			}
			if (EMD == 35)
			{
				Gen_Table(49, 0, 1, ref TempFile);
			}
			if (EMD == 36)
			{
				Gen_Table(49, 0, 2, ref TempFile);
			}
			if (EMD == 37)
			{
				Gen_Table(50, 0, 1, ref TempFile);
			}
			if (EMD == 38)
			{
				Gen_Table(50, 0, 2, ref TempFile);
			}
			if (EMD == 39)
			{
				Gen_Table(51, 0, 0, ref TempFile);
			}
			if (EMD == 40)
			{
				Gen_Table(51, 0, 1, ref TempFile);
			}
			if (EMD == 41)
			{
				Gen_Table(51, 0, 2, ref TempFile);
			}
			if (EMD == 42)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(54, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(53, 0, 0, ref TempFile);
				}
			}
			if (EMD == 43)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(62, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(61, 0, 0, ref TempFile);
				}
			}
			if (EMD == 44)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(56, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(55, 0, 0, ref TempFile);
				}
			}
			if (EMD == 45)
			{
				if (CheckBox1.Checked)
				{
					Gen_Table(58, 0, 0, ref TempFile);
				}
				else
				{
					Gen_Table(57, 0, 0, ref TempFile);
				}
			}
			if (EMD == 46)
			{
				Gen_Table(59, 0, 0, ref TempFile);
			}
			if (EMD == 47)
			{
				Gen_Table(60, 0, 0, ref TempFile);
			}
		}
		if (ComboBox1.SelectedIndex == 5)
		{
			((Control)Export_Grid).Visible = true;
			EMD_MAX = 14;
			if (EMD < 1)
			{
				EMD = 1;
			}
			if ((uint)EMD > (uint)EMD_MAX)
			{
				EMD = EMD_MAX;
			}
			if (EMD == 1)
			{
				Gen_Table(100, 0, 1, ref TempFile);
				Label7.Text = "Upshift";
			}
			if (EMD == 2)
			{
				Gen_Table(100, 0, 2, ref TempFile);
				Label7.Text = "Downshift";
			}
			if (EMD == 3)
			{
				Gen_Table(101, 0, 0, ref TempFile);
			}
			if (EMD == 4)
			{
				Gen_Table(102, 0, 0, ref TempFile);
			}
			if (EMD == 5)
			{
				Gen_Table(103, 0, 0, ref TempFile);
			}
			if (EMD == 6)
			{
				Gen_Table(104, 0, 0, ref TempFile);
			}
			if (EMD == 7)
			{
				Gen_Table(105, 0, 0, ref TempFile);
				Label7.Text = "TCC D1/D2";
			}
			if (EMD == 8)
			{
				Gen_Table(101, 0, 0, ref TempFile);
				Label7.Text = "WOT D2/D3";
			}
			if (EMD == 9)
			{
				Gen_Table(138, 0, 1, ref TempFile);
				Label7.Text = "TUTD Upshift";
			}
			if (EMD == 10)
			{
				Gen_Table(138, 0, 2, ref TempFile);
				Label7.Text = "TUTD Downshift";
			}
			if (EMD == 11)
			{
				Gen_Table(141, 0, 0, ref TempFile);
				Label7.Text = "TUTD WOT";
			}
			if (EMD == 12)
			{
				Gen_Table(139, 0, 0, ref TempFile);
				Label7.Text = "TUTD WOT RPM";
			}
			if (EMD == 13)
			{
				Gen_Table(140, 0, 1, ref TempFile);
				Label7.Text = "TUTD TCC Release";
			}
			if (EMD == 14)
			{
				Gen_Table(140, 0, 2, ref TempFile);
				Label7.Text = "TUTD TCC Apply";
			}
		}
		if ((ComboBox1.SelectedIndex == 6) | (ComboBox1.SelectedIndex == 7))
		{
			((Control)Export_Grid).Visible = true;
			EMD_MAX = 15;
			if (EMD < 1)
			{
				EMD = 1;
			}
			if ((uint)EMD > (uint)EMD_MAX)
			{
				EMD = EMD_MAX;
			}
			if (EMD == 1)
			{
				Gen_Table(100, 0, 1, ref TempFile);
				Label7.Text = "Upshift";
			}
			if (EMD == 2)
			{
				Gen_Table(100, 0, 2, ref TempFile);
				Label7.Text = "Downshift";
			}
			if (EMD == 3)
			{
				Gen_Table(101, 0, 2, ref TempFile);
				Label7.Text = "WOT Upshift";
			}
			if (EMD == 4)
			{
				Gen_Table(101, 0, 1, ref TempFile);
				Label7.Text = "WOT Downshift";
			}
			if (EMD == 5)
			{
				Gen_Table(102, 0, 0, ref TempFile);
			}
			if (EMD == 6)
			{
				Gen_Table(103, 0, 0, ref TempFile);
			}
			if (EMD == 7)
			{
				Gen_Table(104, 0, 0, ref TempFile);
			}
			if (EMD == 8)
			{
				Gen_Table(105, 0, 0, ref TempFile);
				Label7.Text = "TCC D1/D2";
			}
			if (EMD == 9)
			{
				Gen_Table(101, 0, 0, ref TempFile);
				Label7.Text = "WOT D2/D3";
			}
			if (EMD == 10)
			{
				Gen_Table(138, 0, 1, ref TempFile);
				Label7.Text = "TUTD Upshift";
			}
			if (EMD == 11)
			{
				Gen_Table(138, 0, 2, ref TempFile);
				Label7.Text = "TUTD Downshift";
			}
			if (EMD == 12)
			{
				Gen_Table(141, 0, 0, ref TempFile);
				Label7.Text = "TUTD WOT";
			}
			if (EMD == 13)
			{
				Gen_Table(139, 0, 0, ref TempFile);
				Label7.Text = "TUTD WOT RPM";
			}
			if (EMD == 14)
			{
				Gen_Table(140, 0, 1, ref TempFile);
				Label7.Text = "TUTD TCC Release";
			}
			if (EMD == 15)
			{
				Gen_Table(140, 0, 2, ref TempFile);
				Label7.Text = "TUTD TCC Apply";
			}
		}
	}

	private void Button1_Click(object sender, EventArgs e)
	{
		checked
		{
			EMD--;
			if (EMD < 1)
			{
				EMD = 1;
			}
			Update_Export();
		}
	}

	private void Button2_Click(object sender, EventArgs e)
	{
		checked
		{
			EMD++;
		}
		if ((uint)EMD > (uint)EMD_MAX)
		{
			EMD = EMD_MAX;
		}
		Update_Export();
	}

	private void Button3_Click(object sender, EventArgs e)
	{
		if (((Control)Export_Grid).Visible)
		{
			Export_Grid.Select_All();
			Export_Grid.CopyClipboard(0);
		}
	}

	private string Ordinal(int n)
	{
		string[] array = new string[13]
		{
			"", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th",
			"10th", "11th", "12th"
		};
		if (n >= 1 && n <= 12)
		{
			return array[n];
		}
		return Conversions.ToString(n) + "th";
	}

	private void Gen_Table(int ET, ushort tn, byte Split, ref FileStream TempFile)
	{
		byte b = 0;
		table_type tb = default(table_type);
		tb.v = 0;
		switch (ET)
		{
		case 38:
			ET = 1;
			b = 1;
			break;
		case 39:
			ET = 9;
			b = 1;
			break;
		case 40:
			ET = 10;
			b = 1;
			break;
		case 41:
			ET = 1;
			b = 2;
			break;
		case 42:
			ET = 1;
			b = 3;
			break;
		case 43:
			ET = 9;
			b = 2;
			break;
		case 44:
			ET = 9;
			b = 3;
			break;
		case 45:
			ET = 10;
			b = 2;
			break;
		case 46:
			ET = 10;
			b = 3;
			break;
		case 47:
			ET = 4;
			b = 1;
			break;
		case 48:
			ET = 5;
			b = 1;
			break;
		case 49:
			ET = 25;
			b = 1;
			break;
		case 50:
			ET = 19;
			b = 1;
			break;
		case 51:
			ET = 20;
			b = 1;
			break;
		case 52:
			ET = 6;
			b = 1;
			break;
		case 138:
			ET = 100;
			b = 1;
			break;
		case 139:
			ET = 102;
			b = 1;
			break;
		case 140:
			ET = 103;
			b = 1;
			break;
		case 141:
			ET = 100;
			b = 2;
			break;
		}
		checked
		{
			if (ET == 1)
			{
				tb.nm = "Main";
				tb.fw = 3;
				tb.units = "mph";
				string[] xaxis = new string[17]
				{
					"0", "6", "12", "19", "25", "31", "37", "44", "50", "56",
					"62", "69", "75", "81", "87", "94", "100"
				};
				tb.xunits = "%";
				string[] yaxis = new string[6] { "1 -> 2 Shift", "2 -> 3 Shift", "3 -> 4 Shift", "2 -> 1 Shift", "3 -> 2 Shift", "4 -> 3 Shift" };
				tb.yunits = "";
				tb.tn = tn;
				tb.xaxis = xaxis;
				tb.yaxis = yaxis;
				tb.table_x = 17;
				tb.table_y = 6;
				tb.table = new float[tb.table_x + 1, tb.table_y + 1];
				double num = (double)tb.table_y / 2.0;
				for (double num2 = 1.0; num2 <= num; num2 += 1.0)
				{
					int table_x = tb.table_x;
					for (int i = 1; i <= table_x; i++)
					{
						tb.table[i, (int)Math.Round(num2)] = MyProject.Forms.Main_Form.U_Shift.R_Data((byte)i, (byte)Math.Round(num2));
						tb.table[i, (int)Math.Round(num2 + (double)tb.table_y / 2.0)] = MyProject.Forms.Main_Form.D_Shift.R_Data((byte)i, (byte)Math.Round(num2));
					}
				}
				tb.v = 1;
			}
			else if (unchecked(ET == 2 || ET == 3))
			{
				tb.nm = "WOT";
				tb.fw = 3;
				tb.units = "mph";
				if (ET == 3)
				{
					string[] xaxis2 = new string[2] { "0", "100" };
					tb.xunits = "%";
					tb.xaxis = xaxis2;
				}
				else
				{
					string[] xaxis3 = new string[1] { "Speed" };
					tb.xunits = "";
					tb.xaxis = xaxis3;
				}
				string[] yaxis2 = new string[6] { "1 -> 2 Shift", "2 -> 3 Shift", "3 -> 4 Shift", "2 -> 1 Shift", "3 -> 2 Shift", "4 -> 3 Shift" };
				tb.yunits = "";
				tb.tn = tn;
				tb.yaxis = yaxis2;
				if (ET == 3)
				{
					tb.table_x = 2;
				}
				else
				{
					tb.table_x = 1;
				}
				tb.table_y = 6;
				tb.table = new float[tb.table_x + 1, tb.table_y + 1];
				double num3 = (double)tb.table_y / 2.0;
				for (double num4 = 1.0; num4 <= num3; num4 += 1.0)
				{
					int table_x2 = tb.table_x;
					for (int j = 1; j <= table_x2; j++)
					{
						tb.table[j, (int)Math.Round(num4)] = MyProject.Forms.Main_Form.U_Shift.R_Data(17, (byte)Math.Round(num4));
						tb.table[j, (int)Math.Round(num4 + (double)tb.table_y / 2.0)] = MyProject.Forms.Main_Form.D_Shift.R_Data(17, (byte)Math.Round(num4));
					}
				}
				tb.v = 1;
			}
			else if (unchecked(ET == 4 || ET == 5))
			{
				tb.nm = "WOT RPM";
				tb.fw = 4;
				tb.units = "rpm";
				if (ET == 5)
				{
					string[] xaxis4 = new string[2] { "0", "100" };
					tb.xunits = "%";
					tb.xaxis = xaxis4;
				}
				else
				{
					string[] xaxis5 = new string[1] { "RPM" };
					tb.xunits = "";
					tb.xaxis = xaxis5;
				}
				string[] yaxis3 = new string[3] { "1 -> 2 Shift", "2 -> 3 Shift", "3 -> 4 Shift" };
				tb.yunits = "";
				tb.tn = tn;
				tb.yaxis = yaxis3;
				if (ET == 5)
				{
					tb.table_x = 2;
				}
				else
				{
					tb.table_x = 1;
				}
				tb.table_y = 3;
				tb.table = new float[tb.table_x + 1, tb.table_y + 1];
				int table_y = tb.table_y;
				for (int k = 1; k <= table_y; k++)
				{
					float num5;
					if (MyProject.Forms.Lead_Form.Lead_Radio1.Checked)
					{
						num5 = (MyProject.Forms.Main_Form.Speed.R_Data(3, (byte)k) + 5f) / MyProject.Forms.Main_Form.Speed.R_Data(2, (byte)k);
						if (num5 > 1f)
						{
							num5 = 1f;
						}
						num5 = 1f - num5;
						num5 = MyProject.Forms.Main_Form.RPM.R_Data(1, (byte)k) - num5 * MyProject.Forms.Main_Form.RPM.R_Data(1, (byte)k);
					}
					else
					{
						num5 = ((!MyProject.Forms.Main_Form.MaxSpeed_Locked.Checked) ? MyProject.Forms.Main_Form.Speed.R_Data(2, (byte)k) : ((decimal.Compare(new decimal(k), MyProject.Forms.Main_Form.WotLck.Value) < 0) ? MyProject.Forms.Main_Form.Speed.R_Data(2, (byte)k) : MyProject.Forms.Main_Form.Speed.R_Data(1, (byte)k)));
						float num6 = (float)(Convert.ToDouble(MyProject.Forms.Lead_Form.RWHP.Value) * 0.75 * 375.0 / (double)num5 / Convert.ToDouble(MyProject.Forms.Lead_Form.Weight.Value) * 21.93685);
						num5 = ((k > MyProject.Forms.Lead_Form.Delay.Grid_Y) ? ((num5 - num6 * MyProject.Forms.Lead_Form.Delay.R_Data(2, (byte)MyProject.Forms.Lead_Form.Delay.Grid_Y)) / num5) : ((num5 - num6 * MyProject.Forms.Lead_Form.Delay.R_Data(2, (byte)k)) / num5));
						num5 = MyProject.Forms.Main_Form.RPM.R_Data(1, (byte)k) * num5;
					}
					num5 = (int)Math.Round(num5 / 50f) * 50;
					if (MyProject.Forms.Main_Form.LeadRpm.Checked)
					{
						tb.table[1, k] = num5;
					}
					else
					{
						tb.table[1, k] = MyProject.Forms.Main_Form.RPM.R_Data(1, (byte)k);
					}
					if (unchecked(MyProject.Forms.Main_Form.SGS.Checked && k == 1))
					{
						tb.table[1, k] = 0f;
					}
					if (ET == 5)
					{
						tb.table[2, k] = tb.table[1, k];
					}
				}
				tb.v = 1;
			}
			else if (ET == 6)
			{
				tb.nm = "TCC";
				tb.fw = 3;
				tb.units = "mph";
				string[] xaxis6 = new string[17]
				{
					"0", "6", "12", "19", "25", "31", "37", "44", "50", "56",
					"62", "69", "75", "81", "87", "94", "100"
				};
				tb.xunits = "%";
				string[] yaxis4 = new string[6] { "2nd Apply", "3rd Apply", "4th Apply", "2nd Release", "3rd Release", "4th Release" };
				tb.yunits = "";
				tb.tn = tn;
				tb.xaxis = xaxis6;
				tb.yaxis = yaxis4;
				tb.table_x = 17;
				tb.table_y = 6;
				tb.table = new float[tb.table_x + 1, tb.table_y + 1];
				double num7 = (double)tb.table_y / 2.0;
				for (double num8 = 1.0; num8 <= num7; num8 += 1.0)
				{
					int table_x3 = tb.table_x;
					for (int l = 1; l <= table_x3; l++)
					{
						tb.table[l, (int)Math.Round(num8)] = MyProject.Forms.Main_Form.Lock.R_Data((byte)l, (byte)Math.Round(num8 + 1.0));
						tb.table[l, (int)Math.Round(num8 + (double)tb.table_y / 2.0)] = MyProject.Forms.Main_Form.Unlock.R_Data((byte)l, (byte)Math.Round(num8 + 1.0));
					}
				}
				tb.v = 1;
			}
			else if (unchecked(ET == 7 || ET == 8))
			{
				tb.nm = "WOT TCC";
				tb.fw = 3;
				tb.units = "mph";
				if (ET == 8)
				{
					string[] xaxis7 = new string[2] { "0", "100" };
					tb.xunits = "%";
					tb.xaxis = xaxis7;
				}
				else
				{
					string[] xaxis8 = new string[1] { "Speed" };
					tb.xunits = "";
					tb.xaxis = xaxis8;
				}
				string[] yaxis5 = new string[6] { "2nd Apply", "3rd Apply", "4th Apply", "2nd Release", "3rd Release", "4th Release" };
				tb.yunits = "";
				tb.tn = tn;
				tb.yaxis = yaxis5;
				if (ET == 8)
				{
					tb.table_x = 2;
				}
				else
				{
					tb.table_x = 1;
				}
				tb.table_y = 6;
				tb.table = new float[tb.table_x + 1, tb.table_y + 1];
				double num9 = (double)tb.table_y / 2.0;
				for (double num10 = 1.0; num10 <= num9; num10 += 1.0)
				{
					int table_x4 = tb.table_x;
					for (int m = 1; m <= table_x4; m++)
					{
						tb.table[m, (int)Math.Round(num10)] = MyProject.Forms.Main_Form.Lock.R_Data(17, (byte)Math.Round(num10 + 1.0));
						tb.table[m, (int)Math.Round(num10 + (double)tb.table_y / 2.0)] = MyProject.Forms.Main_Form.Unlock.R_Data(17, (byte)Math.Round(num10 + 1.0));
					}
				}
				tb.v = 1;
			}
			else
			{
				switch (ET)
				{
				case 9:
				{
					tb.nm = "5th";
					tb.fw = 3;
					tb.units = "mph";
					string[] xaxis53 = new string[17]
					{
						"0", "6", "12", "19", "25", "31", "37", "44", "50", "56",
						"62", "69", "75", "81", "87", "94", "100"
					};
					tb.xunits = "%";
					string[] yaxis33 = new string[2] { "4 -> 5 Shift", "5 -> 4 Shift" };
					tb.yunits = "";
					tb.tn = tn;
					tb.xaxis = xaxis53;
					tb.yaxis = yaxis33;
					tb.table_x = 17;
					tb.table_y = 2;
					tb.table = new float[tb.table_x + 1, tb.table_y + 1];
					double num86 = (double)tb.table_y / 2.0;
					for (double num87 = 1.0; num87 <= num86; num87 += 1.0)
					{
						int table_x28 = tb.table_x;
						for (int num88 = 1; num88 <= table_x28; num88++)
						{
							tb.table[num88, (int)Math.Round(num87)] = MyProject.Forms.Main_Form.U_Shift.R_Data((byte)num88, 4);
							tb.table[num88, (int)Math.Round(num87 + (double)tb.table_y / 2.0)] = MyProject.Forms.Main_Form.D_Shift.R_Data((byte)num88, 4);
						}
					}
					tb.v = 1;
					break;
				}
				case 10:
				{
					tb.nm = "6th";
					tb.fw = 3;
					tb.units = "mph";
					string[] xaxis52 = new string[17]
					{
						"0", "6", "12", "19", "25", "31", "37", "44", "50", "56",
						"62", "69", "75", "81", "87", "94", "100"
					};
					tb.xunits = "%";
					string[] yaxis32 = new string[2] { "5 -> 6 Shift", "6 -> 5 Shift" };
					tb.yunits = "";
					tb.tn = tn;
					tb.xaxis = xaxis52;
					tb.yaxis = yaxis32;
					tb.table_x = 17;
					tb.table_y = 2;
					tb.table = new float[tb.table_x + 1, tb.table_y + 1];
					double num83 = (double)tb.table_y / 2.0;
					for (double num84 = 1.0; num84 <= num83; num84 += 1.0)
					{
						int table_x27 = tb.table_x;
						for (int num85 = 1; num85 <= table_x27; num85++)
						{
							tb.table[num85, (int)Math.Round(num84)] = MyProject.Forms.Main_Form.U_Shift.R_Data((byte)num85, 5);
							tb.table[num85, (int)Math.Round(num84 + (double)tb.table_y / 2.0)] = MyProject.Forms.Main_Form.D_Shift.R_Data((byte)num85, 5);
						}
					}
					tb.v = 1;
					break;
				}
				default:
					if (unchecked(ET == 11 || ET == 12))
					{
						tb.nm = "5th WOT";
						tb.fw = 3;
						tb.units = "mph";
						if (ET == 12)
						{
							string[] xaxis9 = new string[2] { "0", "100" };
							tb.xunits = "%";
							tb.xaxis = xaxis9;
						}
						else
						{
							string[] xaxis10 = new string[1] { "Speed" };
							tb.xunits = "";
							tb.xaxis = xaxis10;
						}
						string[] yaxis6 = new string[2] { "4 -> 5 Shift", "5 -> 4 Shift" };
						tb.yunits = "";
						tb.tn = tn;
						tb.yaxis = yaxis6;
						if (ET == 12)
						{
							tb.table_x = 2;
						}
						else
						{
							tb.table_x = 1;
						}
						tb.table_y = 2;
						tb.table = new float[tb.table_x + 1, tb.table_y + 1];
						double num11 = (double)tb.table_y / 2.0;
						for (double num12 = 1.0; num12 <= num11; num12 += 1.0)
						{
							int table_x5 = tb.table_x;
							for (int n = 1; n <= table_x5; n++)
							{
								tb.table[n, (int)Math.Round(num12)] = MyProject.Forms.Main_Form.U_Shift.R_Data(17, 4);
								tb.table[n, (int)Math.Round(num12 + (double)tb.table_y / 2.0)] = MyProject.Forms.Main_Form.D_Shift.R_Data(17, 4);
							}
						}
						tb.v = 1;
						break;
					}
					if (unchecked(ET == 13 || ET == 14))
					{
						tb.nm = "6th WOT";
						tb.fw = 3;
						tb.units = "mph";
						if (ET == 14)
						{
							string[] xaxis11 = new string[2] { "0", "100" };
							tb.xunits = "%";
							tb.xaxis = xaxis11;
						}
						else
						{
							string[] xaxis12 = new string[1] { "Speed" };
							tb.xunits = "";
							tb.xaxis = xaxis12;
						}
						string[] yaxis7 = new string[2] { "5 -> 6 Shift", "6 -> 5 Shift" };
						tb.yunits = "";
						tb.tn = tn;
						tb.yaxis = yaxis7;
						if (ET == 14)
						{
							tb.table_x = 2;
						}
						else
						{
							tb.table_x = 1;
						}
						tb.table_y = 2;
						tb.table = new float[tb.table_x + 1, tb.table_y + 1];
						double num13 = (double)tb.table_y / 2.0;
						for (double num14 = 1.0; num14 <= num13; num14 += 1.0)
						{
							int table_x6 = tb.table_x;
							for (int num15 = 1; num15 <= table_x6; num15++)
							{
								tb.table[num15, (int)Math.Round(num14)] = MyProject.Forms.Main_Form.U_Shift.R_Data(17, 5);
								tb.table[num15, (int)Math.Round(num14 + (double)tb.table_y / 2.0)] = MyProject.Forms.Main_Form.D_Shift.R_Data(17, 5);
							}
						}
						tb.v = 1;
						break;
					}
					if (unchecked(ET == 15 || ET == 16))
					{
						tb.nm = "5th WOT RPM";
						tb.fw = 4;
						tb.units = "rpm";
						if (ET == 16)
						{
							string[] xaxis13 = new string[2] { "0", "100" };
							tb.xunits = "%";
							tb.xaxis = xaxis13;
						}
						else
						{
							string[] xaxis14 = new string[1] { "RPM" };
							tb.xunits = "";
							tb.xaxis = xaxis14;
						}
						string[] yaxis8 = new string[1] { "4 -> 5 Shift" };
						tb.yunits = "";
						tb.tn = tn;
						tb.yaxis = yaxis8;
						if (ET == 16)
						{
							tb.table_x = 2;
						}
						else
						{
							tb.table_x = 1;
						}
						tb.table_y = 1;
						tb.table = new float[tb.table_x + 1, tb.table_y + 1];
						float num16;
						if (MyProject.Forms.Lead_Form.Lead_Radio1.Checked)
						{
							num16 = (MyProject.Forms.Main_Form.Speed.R_Data(3, 4) + 5f) / MyProject.Forms.Main_Form.Speed.R_Data(2, 4);
							if (num16 > 1f)
							{
								num16 = 1f;
							}
							num16 = 1f - num16;
							num16 = MyProject.Forms.Main_Form.RPM.R_Data(1, 4) - num16 * MyProject.Forms.Main_Form.RPM.R_Data(1, 4);
						}
						else
						{
							num16 = ((!MyProject.Forms.Main_Form.MaxSpeed_Locked.Checked) ? MyProject.Forms.Main_Form.Speed.R_Data(2, 4) : ((decimal.Compare(4m, MyProject.Forms.Main_Form.WotLck.Value) < 0) ? MyProject.Forms.Main_Form.Speed.R_Data(2, 4) : MyProject.Forms.Main_Form.Speed.R_Data(1, 4)));
							float num17 = (float)(Convert.ToDouble(MyProject.Forms.Lead_Form.RWHP.Value) * 0.75 * 375.0 / (double)num16 / Convert.ToDouble(MyProject.Forms.Lead_Form.Weight.Value) * 21.93685);
							num16 = (num16 - num17 * MyProject.Forms.Lead_Form.Delay.R_Data(2, 4)) / num16;
							num16 = MyProject.Forms.Main_Form.RPM.R_Data(1, 4) * num16;
						}
						num16 = (int)Math.Round(num16 / 50f) * 50;
						if (MyProject.Forms.Main_Form.LeadRpm.Checked)
						{
							tb.table[1, 1] = num16;
						}
						else
						{
							tb.table[1, 1] = MyProject.Forms.Main_Form.RPM.R_Data(1, 4);
						}
						if (ET == 16)
						{
							tb.table[2, 1] = tb.table[1, 1];
						}
						tb.v = 1;
						break;
					}
					if (unchecked(ET == 17 || ET == 18))
					{
						tb.nm = "6th WOT RPM";
						tb.fw = 4;
						tb.units = "rpm";
						if (ET == 18)
						{
							string[] xaxis15 = new string[2] { "0", "100" };
							tb.xunits = "%";
							tb.xaxis = xaxis15;
						}
						else
						{
							string[] xaxis16 = new string[1] { "RPM" };
							tb.xunits = "";
							tb.xaxis = xaxis16;
						}
						string[] yaxis9 = new string[1] { "5 -> 6 Shift" };
						tb.yunits = "";
						tb.tn = tn;
						tb.yaxis = yaxis9;
						if (ET == 18)
						{
							tb.table_x = 2;
						}
						else
						{
							tb.table_x = 1;
						}
						tb.table_y = 1;
						tb.table = new float[tb.table_x + 1, tb.table_y + 1];
						float num18;
						if (MyProject.Forms.Lead_Form.Lead_Radio1.Checked)
						{
							num18 = (MyProject.Forms.Main_Form.Speed.R_Data(3, 5) + 5f) / MyProject.Forms.Main_Form.Speed.R_Data(2, 5);
							if (num18 > 1f)
							{
								num18 = 1f;
							}
							num18 = 1f - num18;
							num18 = MyProject.Forms.Main_Form.RPM.R_Data(1, 5) - num18 * MyProject.Forms.Main_Form.RPM.R_Data(1, 5);
						}
						else
						{
							num18 = ((!MyProject.Forms.Main_Form.MaxSpeed_Locked.Checked) ? MyProject.Forms.Main_Form.Speed.R_Data(2, 5) : ((decimal.Compare(5m, MyProject.Forms.Main_Form.WotLck.Value) < 0) ? MyProject.Forms.Main_Form.Speed.R_Data(2, 5) : MyProject.Forms.Main_Form.Speed.R_Data(1, 5)));
							float num19 = (float)(Convert.ToDouble(MyProject.Forms.Lead_Form.RWHP.Value) * 0.75 * 375.0 / (double)num18 / Convert.ToDouble(MyProject.Forms.Lead_Form.Weight.Value) * 21.93685);
							num18 = (num18 - num19 * MyProject.Forms.Lead_Form.Delay.R_Data(2, 5)) / num18;
							num18 = MyProject.Forms.Main_Form.RPM.R_Data(1, 5) * num18;
						}
						num18 = (int)Math.Round(num18 / 50f) * 50;
						if (MyProject.Forms.Main_Form.LeadRpm.Checked)
						{
							tb.table[1, 1] = num18;
						}
						else
						{
							tb.table[1, 1] = MyProject.Forms.Main_Form.RPM.R_Data(1, 5);
						}
						if (ET == 18)
						{
							tb.table[2, 1] = tb.table[1, 1];
						}
						tb.v = 1;
						break;
					}
					switch (ET)
					{
					case 19:
					{
						tb.nm = "5th TCC";
						tb.fw = 3;
						tb.units = "mph";
						string[] xaxis50 = new string[17]
						{
							"0", "6", "12", "19", "25", "31", "37", "44", "50", "56",
							"62", "69", "75", "81", "87", "94", "100"
						};
						tb.xunits = "%";
						string[] yaxis30 = new string[2] { "5th Apply", "5th Release" };
						tb.yunits = "";
						tb.tn = tn;
						tb.xaxis = xaxis50;
						tb.yaxis = yaxis30;
						tb.table_x = 17;
						tb.table_y = 2;
						tb.table = new float[tb.table_x + 1, tb.table_y + 1];
						double num77 = (double)tb.table_y / 2.0;
						for (double num78 = 1.0; num78 <= num77; num78 += 1.0)
						{
							int table_x25 = tb.table_x;
							for (int num79 = 1; num79 <= table_x25; num79++)
							{
								tb.table[num79, (int)Math.Round(num78)] = MyProject.Forms.Main_Form.Lock.R_Data((byte)num79, 5);
								tb.table[num79, (int)Math.Round(num78 + (double)tb.table_y / 2.0)] = MyProject.Forms.Main_Form.Unlock.R_Data((byte)num79, 5);
							}
						}
						tb.v = 1;
						break;
					}
					case 20:
					{
						tb.nm = "6th TCC";
						tb.fw = 3;
						tb.units = "mph";
						string[] xaxis51 = new string[17]
						{
							"0", "6", "12", "19", "25", "31", "37", "44", "50", "56",
							"62", "69", "75", "81", "87", "94", "100"
						};
						tb.xunits = "%";
						string[] yaxis31 = new string[2] { "6th Apply", "6th Release" };
						tb.yunits = "";
						tb.tn = tn;
						tb.xaxis = xaxis51;
						tb.yaxis = yaxis31;
						tb.table_x = 17;
						tb.table_y = 2;
						tb.table = new float[tb.table_x + 1, tb.table_y + 1];
						double num80 = (double)tb.table_y / 2.0;
						for (double num81 = 1.0; num81 <= num80; num81 += 1.0)
						{
							int table_x26 = tb.table_x;
							for (int num82 = 1; num82 <= table_x26; num82++)
							{
								tb.table[num82, (int)Math.Round(num81)] = MyProject.Forms.Main_Form.Lock.R_Data((byte)num82, 6);
								tb.table[num82, (int)Math.Round(num81 + (double)tb.table_y / 2.0)] = MyProject.Forms.Main_Form.Unlock.R_Data((byte)num82, 6);
							}
						}
						tb.v = 1;
						break;
					}
					default:
						if (unchecked(ET == 21 || ET == 22))
						{
							tb.nm = "5th WOT TCC";
							tb.fw = 3;
							tb.units = "mph";
							if (ET == 22)
							{
								string[] xaxis17 = new string[2] { "0", "100" };
								tb.xunits = "%";
								tb.xaxis = xaxis17;
							}
							else
							{
								string[] xaxis18 = new string[1] { "Speed" };
								tb.xunits = "";
								tb.xaxis = xaxis18;
							}
							string[] yaxis10 = new string[2] { "5th Apply", "5th Release" };
							tb.yunits = "";
							tb.tn = tn;
							tb.yaxis = yaxis10;
							if (ET == 22)
							{
								tb.table_x = 2;
							}
							else
							{
								tb.table_x = 1;
							}
							tb.table_y = 2;
							tb.table = new float[tb.table_x + 1, tb.table_y + 1];
							double num20 = (double)tb.table_y / 2.0;
							for (double num21 = 1.0; num21 <= num20; num21 += 1.0)
							{
								int table_x7 = tb.table_x;
								for (int num22 = 1; num22 <= table_x7; num22++)
								{
									tb.table[num22, (int)Math.Round(num21)] = MyProject.Forms.Main_Form.Lock.R_Data(17, 5);
									tb.table[num22, (int)Math.Round(num21 + (double)tb.table_y / 2.0)] = MyProject.Forms.Main_Form.Unlock.R_Data(17, 5);
								}
							}
							tb.v = 1;
							break;
						}
						if (unchecked(ET == 23 || ET == 24))
						{
							tb.nm = "6th WOT TCC";
							tb.fw = 3;
							tb.units = "mph";
							if (ET == 24)
							{
								string[] xaxis19 = new string[2] { "0", "100" };
								tb.xunits = "%";
								tb.xaxis = xaxis19;
							}
							else
							{
								string[] xaxis20 = new string[1] { "Speed" };
								tb.xunits = "";
								tb.xaxis = xaxis20;
							}
							string[] yaxis11 = new string[2] { "6th Apply", "6th Release" };
							tb.yunits = "";
							tb.tn = tn;
							tb.yaxis = yaxis11;
							if (ET == 24)
							{
								tb.table_x = 2;
							}
							else
							{
								tb.table_x = 1;
							}
							tb.table_y = 2;
							tb.table = new float[tb.table_x + 1, tb.table_y + 1];
							double num23 = (double)tb.table_y / 2.0;
							for (double num24 = 1.0; num24 <= num23; num24 += 1.0)
							{
								int table_x8 = tb.table_x;
								for (int num25 = 1; num25 <= table_x8; num25++)
								{
									tb.table[num25, (int)Math.Round(num24)] = MyProject.Forms.Main_Form.Lock.R_Data(17, 6);
									tb.table[num25, (int)Math.Round(num24 + (double)tb.table_y / 2.0)] = MyProject.Forms.Main_Form.Unlock.R_Data(17, 6);
								}
							}
							tb.v = 1;
							break;
						}
						if (ET == 25)
						{
							tb.nm = "TCC";
							tb.fw = 3;
							tb.units = "mph";
							string[] xaxis21 = new string[17]
							{
								"0", "6", "12", "19", "25", "31", "37", "44", "50", "56",
								"62", "69", "75", "81", "87", "94", "100"
							};
							tb.xunits = "%";
							string[] yaxis12 = new string[8] { "1st Apply", "2nd Apply", "3rd Apply", "4th Apply", "1st Release", "2nd Release", "3rd Release", "4th Release" };
							tb.yunits = "";
							tb.tn = tn;
							tb.xaxis = xaxis21;
							tb.yaxis = yaxis12;
							tb.table_x = 17;
							tb.table_y = 8;
							tb.table = new float[tb.table_x + 1, tb.table_y + 1];
							double num26 = (double)tb.table_y / 2.0;
							for (double num27 = 1.0; num27 <= num26; num27 += 1.0)
							{
								int table_x9 = tb.table_x;
								for (int num28 = 1; num28 <= table_x9; num28++)
								{
									tb.table[num28, (int)Math.Round(num27)] = MyProject.Forms.Main_Form.Lock.R_Data((byte)num28, (byte)Math.Round(num27));
									tb.table[num28, (int)Math.Round(num27 + (double)tb.table_y / 2.0)] = MyProject.Forms.Main_Form.Unlock.R_Data((byte)num28, (byte)Math.Round(num27));
								}
							}
							tb.v = 1;
							break;
						}
						if (unchecked(ET == 26 || ET == 27))
						{
							tb.nm = "WOT TCC";
							tb.fw = 3;
							tb.units = "mph";
							if (ET == 27)
							{
								string[] xaxis22 = new string[2] { "0", "100" };
								tb.xunits = "%";
								tb.xaxis = xaxis22;
							}
							else
							{
								string[] xaxis23 = new string[1] { "Speed" };
								tb.xunits = "";
								tb.xaxis = xaxis23;
							}
							string[] yaxis13 = new string[8] { "1st Apply", "2nd Apply", "3rd Apply", "4th Apply", "1st Release", "2nd Release", "3rd Release", "4th Release" };
							tb.yunits = "";
							tb.tn = tn;
							tb.yaxis = yaxis13;
							if (ET == 27)
							{
								tb.table_x = 2;
							}
							else
							{
								tb.table_x = 1;
							}
							tb.table_y = 8;
							tb.table = new float[tb.table_x + 1, tb.table_y + 1];
							double num29 = (double)tb.table_y / 2.0;
							for (double num30 = 1.0; num30 <= num29; num30 += 1.0)
							{
								int table_x10 = tb.table_x;
								for (int num31 = 1; num31 <= table_x10; num31++)
								{
									tb.table[num31, (int)Math.Round(num30)] = MyProject.Forms.Main_Form.Lock.R_Data(17, (byte)Math.Round(num30));
									tb.table[num31, (int)Math.Round(num30 + (double)tb.table_y / 2.0)] = MyProject.Forms.Main_Form.Unlock.R_Data(17, (byte)Math.Round(num30));
								}
							}
							tb.v = 1;
							break;
						}
						switch (ET)
						{
						case 28:
						{
							tb.nm = "D1";
							tb.fw = 3;
							tb.units = "mph";
							string[] xaxis47 = new string[1] { "Speed" };
							tb.xunits = "";
							tb.xaxis = xaxis47;
							string[] yaxis27 = new string[4] { "1 -> 2 Shift", "2 -> 1 Shift", "2 -> 3 Shift", "3 -> 2 Shift" };
							tb.yunits = "";
							tb.tn = tn;
							tb.yaxis = yaxis27;
							tb.table_x = 1;
							tb.table_y = 4;
							tb.table = new float[tb.table_x + 1, tb.table_y + 1];
							if (!CheckBox11.Checked)
							{
								tb.table[1, 1] = Conversions.ToSingle(MyProject.Forms.Main_Form.Dis_High);
								tb.table[1, 2] = MyProject.Forms.Main_Form.Speed.R_Data(1, 1);
								tb.table[1, 3] = Conversions.ToSingle(MyProject.Forms.Main_Form.Dis_High);
								tb.table[1, 4] = MyProject.Forms.Main_Form.Speed.R_Data(1, 2);
							}
							else
							{
								tb.table[1, 1] = 0f;
								tb.table[1, 2] = 0f;
								tb.table[1, 3] = 0f;
								tb.table[1, 4] = 0f;
							}
							tb.v = 1;
							break;
						}
						case 29:
						{
							tb.nm = "D1 Urban";
							tb.fw = 3;
							tb.units = "mph";
							string[] xaxis44 = new string[17]
							{
								"0", "6", "12", "19", "25", "31", "37", "44", "50", "56",
								"62", "69", "75", "81", "87", "94", "100"
							};
							tb.xunits = "%";
							tb.xaxis = xaxis44;
							string[] yaxis24 = new string[4] { "1 -> 2 Shift", "2 -> 3 Shift", "2 -> 1 Shift", "3 -> 2 Shift" };
							tb.yunits = "";
							tb.tn = tn;
							tb.yaxis = yaxis24;
							tb.table_x = 17;
							tb.table_y = 4;
							tb.table = new float[tb.table_x + 1, tb.table_y + 1];
							int table_x20 = tb.table_x;
							for (int num72 = 1; num72 <= table_x20; num72++)
							{
								if (!CheckBox11.Checked)
								{
									tb.table[num72, 1] = Conversions.ToSingle(MyProject.Forms.Main_Form.Dis_High);
									tb.table[num72, 2] = Conversions.ToSingle(MyProject.Forms.Main_Form.Dis_High);
									tb.table[num72, 3] = MyProject.Forms.Main_Form.Speed.R_Data(1, 1);
									tb.table[num72, 4] = MyProject.Forms.Main_Form.Speed.R_Data(1, 2);
								}
								else
								{
									tb.table[num72, 1] = 0f;
									tb.table[num72, 2] = 0f;
									tb.table[num72, 3] = 0f;
									tb.table[num72, 4] = 0f;
								}
							}
							tb.v = 1;
							break;
						}
						case 30:
						{
							tb.nm = "D2";
							tb.fw = 3;
							tb.units = "mph";
							string[] xaxis49 = new string[17]
							{
								"0", "6", "12", "19", "25", "31", "37", "44", "50", "56",
								"62", "69", "75", "81", "87", "94", "100"
							};
							tb.xunits = "%";
							tb.xaxis = xaxis49;
							string[] yaxis29 = new string[2] { "1 -> 2 Shift", "2 -> 1 Shift" };
							tb.yunits = "";
							tb.tn = tn;
							tb.yaxis = yaxis29;
							tb.table_x = 17;
							tb.table_y = 2;
							tb.table = new float[tb.table_x + 1, tb.table_y + 1];
							int table_x24 = tb.table_x;
							for (int num76 = 1; num76 <= table_x24; num76++)
							{
								if (!CheckBox11.Checked)
								{
									tb.table[num76, 1] = MyProject.Forms.Main_Form.U_Shift.R_Data((byte)num76, 1);
									tb.table[num76, 2] = MyProject.Forms.Main_Form.D_Shift.R_Data((byte)num76, 1);
								}
								else
								{
									tb.table[num76, 1] = 0f;
									tb.table[num76, 2] = 0f;
								}
							}
							tb.v = 1;
							break;
						}
						case 31:
						{
							tb.nm = "D2 3rd";
							tb.fw = 3;
							tb.units = "mph";
							string[] xaxis42 = new string[1] { "Speed" };
							tb.xunits = "";
							tb.xaxis = xaxis42;
							string[] yaxis22 = new string[2] { "2 -> 3 Shift", "3 -> 2 Shift" };
							tb.yunits = "";
							tb.tn = tn;
							tb.yaxis = yaxis22;
							tb.table_x = 1;
							tb.table_y = 2;
							tb.table = new float[tb.table_x + 1, tb.table_y + 1];
							if (!CheckBox11.Checked)
							{
								tb.table[1, 1] = Conversions.ToSingle(MyProject.Forms.Main_Form.Dis_High);
								tb.table[1, 2] = MyProject.Forms.Main_Form.Speed.R_Data(1, 2);
							}
							else
							{
								tb.table[1, 1] = 0f;
								tb.table[1, 2] = 0f;
							}
							tb.v = 1;
							break;
						}
						case 32:
						{
							tb.nm = "TCC Release TPS";
							tb.fw = 3;
							tb.units = "%";
							string[] xaxis46 = new string[17]
							{
								"0", "8", "16", "24", "32", "40", "48", "56", "64", "72",
								"80", "88", "96", "104", "112", "120", "128"
							};
							tb.xunits = "mph";
							tb.xaxis = xaxis46;
							string[] yaxis26 = new string[3] { "2nd Release", "3rd Release", "4th Release" };
							tb.yunits = "";
							tb.tn = tn;
							tb.yaxis = yaxis26;
							tb.table_x = 17;
							tb.table_y = 3;
							tb.table = new float[tb.table_x + 1, tb.table_y + 1];
							int table_x22 = tb.table_x;
							for (int num74 = 1; num74 <= table_x22; num74++)
							{
								tb.table[num74, 1] = 100f;
								tb.table[num74, 2] = 100f;
								tb.table[num74, 3] = 100f;
							}
							tb.v = 1;
							break;
						}
						case 33:
						{
							tb.nm = "D1";
							tb.fw = 3;
							tb.units = "mph";
							string[] xaxis41 = new string[17]
							{
								"0", "6", "12", "19", "25", "31", "37", "44", "50", "56",
								"62", "69", "75", "81", "87", "94", "100"
							};
							tb.xunits = "%";
							tb.xaxis = xaxis41;
							string[] yaxis21 = new string[2] { "1 -> 2 Shift", "2 -> 1 Shift" };
							tb.yunits = "";
							tb.tn = tn;
							tb.yaxis = yaxis21;
							tb.table_x = 17;
							tb.table_y = 2;
							tb.table = new float[tb.table_x + 1, tb.table_y + 1];
							int table_x18 = tb.table_x;
							for (int num70 = 1; num70 <= table_x18; num70++)
							{
								if (!CheckBox11.Checked)
								{
									tb.table[num70, 1] = Conversions.ToSingle(MyProject.Forms.Main_Form.Dis_High);
									tb.table[num70, 2] = MyProject.Forms.Main_Form.Speed.R_Data(1, 1);
								}
								else
								{
									tb.table[num70, 1] = 0f;
									tb.table[num70, 2] = 0f;
								}
							}
							tb.v = 1;
							break;
						}
						case 34:
						{
							tb.nm = "TCC D2";
							tb.fw = 3;
							tb.units = "mph";
							string[] xaxis45 = new string[17]
							{
								"0", "6", "12", "19", "25", "31", "37", "44", "50", "56",
								"62", "69", "75", "81", "87", "94", "100"
							};
							tb.xunits = "%";
							tb.xaxis = xaxis45;
							string[] yaxis25 = new string[2] { "2nd Apply", "2nd Release" };
							tb.yunits = "";
							tb.tn = tn;
							tb.yaxis = yaxis25;
							tb.table_x = 17;
							tb.table_y = 2;
							tb.table = new float[tb.table_x + 1, tb.table_y + 1];
							int table_x21 = tb.table_x;
							for (int num73 = 1; num73 <= table_x21; num73++)
							{
								if (!CheckBox11.Checked)
								{
									tb.table[num73, 1] = MyProject.Forms.Main_Form.Lock.R_Data((byte)num73, 2);
									tb.table[num73, 2] = MyProject.Forms.Main_Form.Unlock.R_Data((byte)num73, 2);
								}
								else
								{
									tb.table[num73, 1] = 0f;
									tb.table[num73, 2] = 0f;
								}
							}
							tb.v = 1;
							break;
						}
						case 35:
						{
							tb.nm = "TCC D1";
							tb.fw = 3;
							tb.units = "mph";
							string[] xaxis43 = new string[17]
							{
								"0", "6", "12", "19", "25", "31", "37", "44", "50", "56",
								"62", "69", "75", "81", "87", "94", "100"
							};
							tb.xunits = "%";
							tb.xaxis = xaxis43;
							string[] yaxis23 = new string[2] { "2nd Apply", "2nd Release" };
							tb.yunits = "";
							tb.tn = tn;
							tb.yaxis = yaxis23;
							tb.table_x = 17;
							tb.table_y = 2;
							tb.table = new float[tb.table_x + 1, tb.table_y + 1];
							int table_x19 = tb.table_x;
							for (int num71 = 1; num71 <= table_x19; num71++)
							{
								if (!CheckBox11.Checked)
								{
									tb.table[num71, 1] = Conversions.ToSingle(MyProject.Forms.Main_Form.Dis_High);
									tb.table[num71, 2] = Conversions.ToSingle(MyProject.Forms.Main_Form.Dis_Low);
								}
								else
								{
									tb.table[num71, 1] = 0f;
									tb.table[num71, 2] = 0f;
								}
							}
							tb.v = 1;
							break;
						}
						case 36:
						{
							tb.nm = "TCC D1/D2";
							tb.fw = 3;
							tb.units = "mph";
							string[] xaxis48 = new string[17]
							{
								"0", "6", "12", "19", "25", "31", "37", "44", "50", "56",
								"62", "69", "75", "81", "87", "94", "100"
							};
							tb.xunits = "%";
							tb.xaxis = xaxis48;
							string[] yaxis28 = new string[4] { "1st Apply", "2nd Apply", "1st Release", "2nd Release" };
							tb.yunits = "";
							tb.tn = tn;
							tb.yaxis = yaxis28;
							tb.table_x = 17;
							tb.table_y = 4;
							tb.table = new float[tb.table_x + 1, tb.table_y + 1];
							int table_x23 = tb.table_x;
							for (int num75 = 1; num75 <= table_x23; num75++)
							{
								if (!CheckBox11.Checked)
								{
									tb.table[num75, 1] = MyProject.Forms.Main_Form.Lock.R_Data((byte)num75, 1);
									tb.table[num75, 2] = MyProject.Forms.Main_Form.Lock.R_Data((byte)num75, 2);
									tb.table[num75, 3] = MyProject.Forms.Main_Form.Unlock.R_Data((byte)num75, 1);
									tb.table[num75, 4] = MyProject.Forms.Main_Form.Unlock.R_Data((byte)num75, 2);
								}
								else
								{
									tb.table[num75, 1] = 0f;
									tb.table[num75, 2] = 0f;
									tb.table[num75, 3] = 0f;
									tb.table[num75, 4] = 0f;
								}
							}
							tb.v = 1;
							break;
						}
						case 37:
						{
							tb.nm = "TUTD";
							tb.fw = 3;
							tb.units = "mph";
							string[] xaxis40 = new string[17]
							{
								"0", "6", "12", "19", "25", "31", "37", "44", "50", "56",
								"62", "69", "75", "81", "87", "94", "100"
							};
							tb.xunits = "%";
							string[] yaxis20 = new string[6] { "1 -> 2 Shift", "2 -> 1 Shift", "2 -> 3 Shift", "3 -> 2 Shift", "3 -> 4 Shift", "4 -> 3 Shift" };
							tb.yunits = "";
							tb.tn = tn;
							tb.xaxis = xaxis40;
							tb.yaxis = yaxis20;
							tb.table_x = 17;
							tb.table_y = 6;
							tb.table = new float[tb.table_x + 1, tb.table_y + 1];
							double num67 = (double)tb.table_y / 2.0;
							for (double num68 = 1.0; num68 <= num67; num68 += 1.0)
							{
								int table_x17 = tb.table_x;
								for (int num69 = 1; num69 <= table_x17; num69++)
								{
									if (CheckBox8.Checked)
									{
										tb.table[num69, (int)Math.Round(num68 * 2.0 - 1.0)] = MyProject.Forms.Main_Form.U_Shift.R_Data(17, (byte)Math.Round(num68));
									}
									else
									{
										tb.table[num69, (int)Math.Round(num68 * 2.0 - 1.0)] = Conversions.ToSingle(MyProject.Forms.Main_Form.Dis_High);
									}
									if (num68 == 1.0)
									{
										tb.table[num69, (int)Math.Round(num68 * 2.0)] = 0f;
									}
									else
									{
										tb.table[num69, (int)Math.Round(num68 * 2.0)] = MyProject.Forms.Main_Form.D_Shift.R_Data(1, (byte)Math.Round(num68));
									}
								}
							}
							tb.v = 1;
							break;
						}
						default:
							if (unchecked(ET == 53 || ET == 54))
							{
								tb.nm = "Saftey D1/D2";
								tb.fw = 3;
								tb.units = "mph";
								if (ET == 54)
								{
									string[] xaxis24 = new string[2] { "0", "100" };
									tb.xunits = "%";
									tb.xaxis = xaxis24;
								}
								else
								{
									string[] xaxis25 = new string[1] { "Speed" };
									tb.xunits = "";
									tb.xaxis = xaxis25;
								}
								string[] yaxis14 = new string[4] { "2 -> 3 Shift", "3 -> 4 Shift", "3 -> 2 Shift", "4 -> 3 Shift" };
								tb.yunits = "";
								tb.tn = tn;
								tb.yaxis = yaxis14;
								if (ET == 54)
								{
									tb.table_x = 2;
								}
								else
								{
									tb.table_x = 1;
								}
								tb.table_y = 4;
								tb.table = new float[tb.table_x + 1, tb.table_y + 1];
								int table_x11 = tb.table_x;
								for (int num32 = 1; num32 <= table_x11; num32++)
								{
									if (!CheckBox12.Checked)
									{
										tb.table[num32, 1] = Conversions.ToSingle(MyProject.Forms.Main_Form.Dis_High);
										tb.table[num32, 2] = Conversions.ToSingle(MyProject.Forms.Main_Form.Dis_High);
										tb.table[num32, 3] = MyProject.Forms.Main_Form.Speed.R_Data(1, 2);
										tb.table[num32, 4] = MyProject.Forms.Main_Form.Speed.R_Data(1, 3);
									}
									else
									{
										tb.table[num32, 1] = 0f;
										tb.table[num32, 2] = 0f;
										tb.table[num32, 3] = 0f;
										tb.table[num32, 4] = 0f;
									}
								}
								tb.v = 1;
								break;
							}
							if (unchecked(ET == 55 || ET == 56))
							{
								tb.nm = "5th Saftey";
								tb.fw = 3;
								tb.units = "mph";
								if (ET == 56)
								{
									string[] xaxis26 = new string[2] { "0", "100" };
									tb.xunits = "%";
									tb.xaxis = xaxis26;
								}
								else
								{
									string[] xaxis27 = new string[1] { "Speed" };
									tb.xunits = "";
									tb.xaxis = xaxis27;
								}
								string[] yaxis15 = new string[2] { "4 -> 5 Shift", "5 -> 4 Shift" };
								tb.yunits = "";
								tb.tn = tn;
								tb.yaxis = yaxis15;
								if (ET == 56)
								{
									tb.table_x = 2;
								}
								else
								{
									tb.table_x = 1;
								}
								tb.table_y = 2;
								tb.table = new float[tb.table_x + 1, tb.table_y + 1];
								int table_x12 = tb.table_x;
								for (int num33 = 1; num33 <= table_x12; num33++)
								{
									if (!CheckBox12.Checked)
									{
										tb.table[num33, 1] = Conversions.ToSingle(MyProject.Forms.Main_Form.Dis_High);
										tb.table[num33, 2] = MyProject.Forms.Main_Form.Speed.R_Data(1, 4);
									}
									else
									{
										tb.table[num33, 1] = 0f;
										tb.table[num33, 2] = 0f;
									}
								}
								tb.v = 1;
								break;
							}
							if (unchecked(ET == 57 || ET == 58))
							{
								tb.nm = "6th Saftey";
								tb.fw = 3;
								tb.units = "mph";
								if (ET == 58)
								{
									string[] xaxis28 = new string[2] { "0", "100" };
									tb.xunits = "%";
									tb.xaxis = xaxis28;
								}
								else
								{
									string[] xaxis29 = new string[1] { "Speed" };
									tb.xunits = "";
									tb.xaxis = xaxis29;
								}
								string[] yaxis16 = new string[2] { "5 -> 6 Shift", "6 -> 5 Shift" };
								tb.yunits = "";
								tb.tn = tn;
								tb.yaxis = yaxis16;
								if (ET == 58)
								{
									tb.table_x = 2;
								}
								else
								{
									tb.table_x = 1;
								}
								tb.table_y = 2;
								tb.table = new float[tb.table_x + 1, tb.table_y + 1];
								int table_x13 = tb.table_x;
								for (int num34 = 1; num34 <= table_x13; num34++)
								{
									if (!CheckBox12.Checked)
									{
										tb.table[num34, 1] = Conversions.ToSingle(MyProject.Forms.Main_Form.Dis_High);
										tb.table[num34, 2] = MyProject.Forms.Main_Form.Speed.R_Data(1, 5);
									}
									else
									{
										tb.table[num34, 1] = 0f;
										tb.table[num34, 2] = 0f;
									}
								}
								tb.v = 1;
								break;
							}
							switch (ET)
							{
							case 59:
							{
								tb.nm = "5th Saftey";
								tb.fw = 3;
								tb.units = "mph";
								string[] xaxis39 = new string[17]
								{
									"0", "6", "12", "19", "25", "31", "37", "44", "50", "56",
									"62", "69", "75", "81", "87", "94", "100"
								};
								tb.xunits = "%";
								string[] yaxis19 = new string[2] { "4 -> 5 Shift", "5 -> 4 Shift" };
								tb.yunits = "";
								tb.tn = tn;
								tb.xaxis = xaxis39;
								tb.yaxis = yaxis19;
								tb.table_x = 17;
								tb.table_y = 2;
								tb.table = new float[tb.table_x + 1, tb.table_y + 1];
								double num64 = (double)tb.table_y / 2.0;
								for (double num65 = 1.0; num65 <= num64; num65 += 1.0)
								{
									int table_x16 = tb.table_x;
									for (int num66 = 1; num66 <= table_x16; num66++)
									{
										if (!CheckBox12.Checked)
										{
											tb.table[num66, (int)Math.Round(num65)] = Conversions.ToSingle(MyProject.Forms.Main_Form.Dis_High);
											tb.table[num66, (int)Math.Round(num65 + (double)tb.table_y / 2.0)] = MyProject.Forms.Main_Form.Speed.R_Data(1, 4);
										}
										else
										{
											tb.table[num66, (int)Math.Round(num65)] = 0f;
											tb.table[num66, (int)Math.Round(num65 + (double)tb.table_y / 2.0)] = 0f;
										}
									}
								}
								tb.v = 1;
								break;
							}
							case 60:
							{
								tb.nm = "6th Saftey";
								tb.fw = 3;
								tb.units = "mph";
								string[] xaxis38 = new string[17]
								{
									"0", "6", "12", "19", "25", "31", "37", "44", "50", "56",
									"62", "69", "75", "81", "87", "94", "100"
								};
								tb.xunits = "%";
								string[] yaxis18 = new string[2] { "5 -> 6 Shift", "6 -> 5 Shift" };
								tb.yunits = "";
								tb.tn = tn;
								tb.xaxis = xaxis38;
								tb.yaxis = yaxis18;
								tb.table_x = 17;
								tb.table_y = 2;
								tb.table = new float[tb.table_x + 1, tb.table_y + 1];
								double num61 = (double)tb.table_y / 2.0;
								for (double num62 = 1.0; num62 <= num61; num62 += 1.0)
								{
									int table_x15 = tb.table_x;
									for (int num63 = 1; num63 <= table_x15; num63++)
									{
										if (!CheckBox12.Checked)
										{
											tb.table[num63, (int)Math.Round(num62)] = Conversions.ToSingle(MyProject.Forms.Main_Form.Dis_High);
											tb.table[num63, (int)Math.Round(num62 + (double)tb.table_y / 2.0)] = MyProject.Forms.Main_Form.Speed.R_Data(1, 5);
										}
										else
										{
											tb.table[num63, (int)Math.Round(num62)] = 0f;
											tb.table[num63, (int)Math.Round(num62 + (double)tb.table_y / 2.0)] = 0f;
										}
									}
								}
								tb.v = 1;
								break;
							}
							default:
								if (unchecked(ET == 61 || ET == 62))
								{
									tb.nm = "Saftey D3";
									tb.fw = 3;
									tb.units = "mph";
									if (ET == 62)
									{
										string[] xaxis30 = new string[2] { "0", "100" };
										tb.xunits = "%";
										tb.xaxis = xaxis30;
									}
									else
									{
										string[] xaxis31 = new string[1] { "Speed" };
										tb.xunits = "";
										tb.xaxis = xaxis31;
									}
									string[] yaxis17 = new string[2] { "3 -> 4 Shift", "4 -> 3 Shift" };
									tb.yunits = "";
									tb.tn = tn;
									tb.yaxis = yaxis17;
									if (ET == 62)
									{
										tb.table_x = 2;
									}
									else
									{
										tb.table_x = 1;
									}
									tb.table_y = 2;
									tb.table = new float[tb.table_x + 1, tb.table_y + 1];
									int table_x14 = tb.table_x;
									for (int num35 = 1; num35 <= table_x14; num35++)
									{
										if (!CheckBox12.Checked)
										{
											tb.table[num35, 1] = Conversions.ToSingle(MyProject.Forms.Main_Form.Dis_High);
											tb.table[num35, 2] = MyProject.Forms.Main_Form.Speed.R_Data(1, 3);
										}
										else
										{
											tb.table[num35, 1] = 0f;
											tb.table[num35, 2] = 0f;
										}
									}
									tb.v = 1;
									break;
								}
								switch (ET)
								{
								case 100:
								{
									int num42 = Convert.ToInt32(MyProject.Forms.Main_Form.Gears.Value);
									int num43 = num42;
									if ((ComboBox1.SelectedIndex == 6) | (ComboBox1.SelectedIndex == 7))
									{
										num43 = 10;
									}
									tb.nm = "Main";
									tb.fw = 3;
									tb.units = "mph";
									string[] xaxis34 = new string[17]
									{
										"0", "6", "12", "19", "25", "31", "37", "44", "50", "56",
										"62", "69", "75", "81", "87", "94", "100"
									};
									tb.xunits = "";
									tb.xaxis = xaxis34;
									tb.table_x = 17;
									tb.table_y = (num43 - 1) * 2;
									tb.table = new float[tb.table_x + 1, tb.table_y + 1];
									tb.yaxis = new string[tb.table_y - 1 + 1];
									int num44 = num43 - 1;
									for (int num45 = 1; num45 <= num44; num45++)
									{
										tb.yaxis[num45 - 1] = Conversions.ToString(num45) + " -> " + Conversions.ToString(num45 + 1) + " Shift";
										tb.yaxis[num45 - 1 + (num43 - 1)] = Conversions.ToString(num45 + 1) + " -> " + Conversions.ToString(num45) + " Downshift";
										int num46 = 1;
										do
										{
											if (num45 <= num42 - 1)
											{
												tb.table[num46, num45] = MyProject.Forms.Main_Form.U_Shift.R_Data((byte)num46, (byte)num45);
												tb.table[num46, num45 + (num43 - 1)] = MyProject.Forms.Main_Form.D_Shift.R_Data((byte)num46, (byte)num45);
											}
											else
											{
												tb.table[num46, num45] = Conversions.ToSingle(MyProject.Forms.Main_Form.Dis_High);
												tb.table[num46, num45 + (num43 - 1)] = Conversions.ToSingle(MyProject.Forms.Main_Form.Dis_Low);
											}
											num46++;
										}
										while (num46 <= 17);
									}
									tb.tn = tn;
									tb.v = 1;
									break;
								}
								case 101:
								{
									int num38 = Convert.ToInt32(MyProject.Forms.Main_Form.Gears.Value);
									int num39 = num38;
									if ((ComboBox1.SelectedIndex == 6) | (ComboBox1.SelectedIndex == 7))
									{
										num39 = 10;
									}
									tb.nm = "WOT";
									tb.fw = 3;
									tb.units = "mph";
									string[] xaxis33 = new string[1] { "Shift MPH" };
									tb.xunits = "";
									tb.xaxis = xaxis33;
									tb.table_x = 1;
									tb.table_y = (num39 - 1) * 2;
									tb.table = new float[tb.table_x + 1, tb.table_y + 1];
									tb.yaxis = new string[tb.table_y - 1 + 1];
									int num40 = num39 - 1;
									for (int num41 = 1; num41 <= num40; num41++)
									{
										tb.yaxis[num41 - 1] = Conversions.ToString(num41 + 1) + " -> " + Conversions.ToString(num41) + " Downshift";
										tb.yaxis[num41 - 1 + (num39 - 1)] = Conversions.ToString(num41) + " -> " + Conversions.ToString(num41 + 1) + " Upshift";
										if (num41 <= num38 - 1)
										{
											tb.table[1, num41] = MyProject.Forms.Main_Form.D_Shift.R_Data(17, (byte)num41);
											tb.table[1, num41 + (num39 - 1)] = MyProject.Forms.Main_Form.U_Shift.R_Data(17, (byte)num41);
										}
										else
										{
											tb.table[1, num41] = Conversions.ToSingle(MyProject.Forms.Main_Form.Dis_Low);
											tb.table[1, num41 + (num39 - 1)] = Conversions.ToSingle(MyProject.Forms.Main_Form.Dis_High);
										}
									}
									tb.tn = tn;
									tb.v = 1;
									break;
								}
								case 102:
								{
									int num51 = Convert.ToInt32(MyProject.Forms.Main_Form.Gears.Value);
									int num52 = num51;
									if ((ComboBox1.SelectedIndex == 6) | (ComboBox1.SelectedIndex == 7))
									{
										num52 = 10;
									}
									tb.nm = "WOT RPM";
									tb.fw = 4;
									tb.units = "rpm";
									string[] xaxis36 = new string[1] { "RPM" };
									tb.xunits = "";
									tb.xaxis = xaxis36;
									tb.table_x = 1;
									tb.table_y = num52 - 1;
									tb.table = new float[tb.table_x + 1, tb.table_y + 1];
									tb.yaxis = new string[tb.table_y - 1 + 1];
									int table_y2 = tb.table_y;
									for (int num53 = 1; num53 <= table_y2; num53++)
									{
										tb.yaxis[num53 - 1] = Conversions.ToString(num53) + " -> " + Conversions.ToString(num53 + 1) + " Shift";
										if (num53 > num51 - 1)
										{
											tb.table[1, num53] = 8192f;
											continue;
										}
										float num54;
										if (MyProject.Forms.Lead_Form.Lead_Radio1.Checked)
										{
											num54 = (MyProject.Forms.Main_Form.Speed.R_Data(3, (byte)num53) + 5f) / MyProject.Forms.Main_Form.Speed.R_Data(2, (byte)num53);
											if (num54 > 1f)
											{
												num54 = 1f;
											}
											num54 = 1f - num54;
											num54 = MyProject.Forms.Main_Form.RPM.R_Data(1, (byte)num53) - num54 * MyProject.Forms.Main_Form.RPM.R_Data(1, (byte)num53);
										}
										else
										{
											num54 = ((!MyProject.Forms.Main_Form.MaxSpeed_Locked.Checked) ? MyProject.Forms.Main_Form.Speed.R_Data(2, (byte)num53) : ((decimal.Compare(new decimal(num53), MyProject.Forms.Main_Form.WotLck.Value) < 0) ? MyProject.Forms.Main_Form.Speed.R_Data(2, (byte)num53) : MyProject.Forms.Main_Form.Speed.R_Data(1, (byte)num53)));
											float num55 = (float)(Convert.ToDouble(MyProject.Forms.Lead_Form.RWHP.Value) * 0.75 * 375.0 / (double)num54 / Convert.ToDouble(MyProject.Forms.Lead_Form.Weight.Value) * 21.93685);
											num54 = ((num53 > MyProject.Forms.Lead_Form.Delay.Grid_Y) ? ((num54 - num55 * MyProject.Forms.Lead_Form.Delay.R_Data(2, (byte)MyProject.Forms.Lead_Form.Delay.Grid_Y)) / num54) : ((num54 - num55 * MyProject.Forms.Lead_Form.Delay.R_Data(2, (byte)num53)) / num54));
											num54 = MyProject.Forms.Main_Form.RPM.R_Data(1, (byte)num53) * num54;
										}
										num54 = (int)Math.Round(num54 / 50f) * 50;
										if (MyProject.Forms.Main_Form.LeadRpm.Checked)
										{
											tb.table[1, num53] = num54;
										}
										else
										{
											tb.table[1, num53] = MyProject.Forms.Main_Form.RPM.R_Data(1, (byte)num53);
										}
										if (unchecked(MyProject.Forms.Main_Form.SGS.Checked && num53 == 1))
										{
											tb.table[1, num53] = 0f;
										}
									}
									tb.tn = tn;
									tb.v = 1;
									break;
								}
								case 103:
								{
									int num56 = Convert.ToInt32(MyProject.Forms.Main_Form.Gears.Value);
									int num57 = num56;
									if ((ComboBox1.SelectedIndex == 6) | (ComboBox1.SelectedIndex == 7))
									{
										num57 = 10;
									}
									tb.nm = "TCC";
									tb.fw = 3;
									tb.units = "mph";
									string[] xaxis37 = new string[17]
									{
										"0", "6", "12", "19", "25", "31", "37", "44", "50", "56",
										"62", "69", "75", "81", "87", "94", "100"
									};
									tb.xunits = "%";
									tb.xaxis = xaxis37;
									tb.table_x = 17;
									tb.table_y = num57 * 2;
									tb.table = new float[tb.table_x + 1, tb.table_y + 1];
									tb.yaxis = new string[tb.table_y - 1 + 1];
									int num58 = num57;
									for (int num59 = 1; num59 <= num58; num59++)
									{
										tb.yaxis[num59 - 1] = Ordinal(num59) + " Release";
										tb.yaxis[num59 - 1 + num57] = Ordinal(num59) + " Apply";
										int num60 = 1;
										do
										{
											if (num59 <= num56)
											{
												tb.table[num60, num59] = MyProject.Forms.Main_Form.Unlock.R_Data((byte)num60, (byte)num59);
												tb.table[num60, num59 + num57] = MyProject.Forms.Main_Form.Lock.R_Data((byte)num60, (byte)num59);
											}
											else
											{
												tb.table[num60, num59] = Conversions.ToSingle(MyProject.Forms.Main_Form.Dis_Low);
												tb.table[num60, num59 + num57] = Conversions.ToSingle(MyProject.Forms.Main_Form.Dis_High);
											}
											num60++;
										}
										while (num60 <= 17);
									}
									tb.tn = tn;
									tb.v = 1;
									break;
								}
								case 104:
								{
									int num47 = Convert.ToInt32(MyProject.Forms.Main_Form.Gears.Value);
									int num48 = num47;
									if ((ComboBox1.SelectedIndex == 6) | (ComboBox1.SelectedIndex == 7))
									{
										num48 = 10;
									}
									tb.nm = "TCC WOT";
									tb.fw = 3;
									tb.units = "mph";
									string[] xaxis35 = new string[1] { "Speed" };
									tb.xunits = "";
									tb.xaxis = xaxis35;
									tb.table_x = 1;
									tb.table_y = num48 * 2;
									tb.table = new float[tb.table_x + 1, tb.table_y + 1];
									tb.yaxis = new string[tb.table_y - 1 + 1];
									int num49 = num48;
									for (int num50 = 1; num50 <= num49; num50++)
									{
										tb.yaxis[num50 - 1] = Ordinal(num50) + " Release";
										tb.yaxis[num50 - 1 + num48] = Ordinal(num50) + " Apply";
										if (num50 <= num47)
										{
											tb.table[1, num50] = MyProject.Forms.Main_Form.Unlock.R_Data(17, (byte)num50);
											tb.table[1, num50 + num48] = MyProject.Forms.Main_Form.Lock.R_Data(17, (byte)num50);
										}
										else
										{
											tb.table[1, num50] = Conversions.ToSingle(MyProject.Forms.Main_Form.Dis_Low);
											tb.table[1, num50 + num48] = Conversions.ToSingle(MyProject.Forms.Main_Form.Dis_High);
										}
									}
									tb.tn = tn;
									tb.v = 1;
									break;
								}
								case 105:
								{
									tb.nm = "TCC D";
									tb.fw = 3;
									tb.units = "mph";
									string[] xaxis32 = new string[17]
									{
										"0", "6", "12", "19", "25", "31", "37", "44", "50", "56",
										"62", "69", "75", "81", "87", "94", "100"
									};
									tb.xunits = "%";
									tb.xaxis = xaxis32;
									tb.table_x = 17;
									tb.table_y = 4;
									tb.table = new float[tb.table_x + 1, tb.table_y + 1];
									tb.yaxis = new string[tb.table_y - 1 + 1];
									int num36 = 1;
									do
									{
										tb.yaxis[num36 - 1] = Ordinal(num36) + " Release";
										tb.yaxis[num36 - 1 + 2] = Ordinal(num36) + " Apply";
										int num37 = 1;
										do
										{
											tb.table[num37, num36] = MyProject.Forms.Main_Form.Unlock.R_Data((byte)num37, (byte)num36);
											tb.table[num37, num36 + 2] = MyProject.Forms.Main_Form.Lock.R_Data((byte)num37, (byte)num36);
											num37++;
										}
										while (num37 <= 17);
										num36++;
									}
									while (num36 <= 2);
									tb.tn = tn;
									tb.v = 1;
									break;
								}
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
			if (unchecked(b >= 1 && b <= 3))
			{
				if (unchecked(ET == 1 || ET == 9 || ET == 10 || ET == 100))
				{
					if (ET == 1)
					{
						tb.nm = "TUTD";
					}
					if (ET == 9)
					{
						tb.nm = "5th TUTD";
					}
					if (ET == 10)
					{
						tb.nm = "6th TUTD";
					}
					if (ET == 100)
					{
						tb.nm = "TUTD";
					}
					double num89 = (double)tb.table_y / 2.0;
					for (double num90 = 1.0; num90 <= num89; num90 += 1.0)
					{
						int table_x29 = tb.table_x;
						for (int num91 = 1; num91 <= table_x29; num91++)
						{
							if (CheckBox8.Checked)
							{
								tb.table[num91, (int)Math.Round(num90)] = tb.table[17, (int)Math.Round(num90)];
							}
							else
							{
								tb.table[num91, (int)Math.Round(num90)] = Conversions.ToSingle(MyProject.Forms.Main_Form.Dis_High);
							}
							if (unchecked((ET == 1 || ET == 100) && num90 == 1.0))
							{
								tb.table[num91, (int)Math.Round(num90 + (double)tb.table_y / 2.0)] = 0f;
							}
							else
							{
								tb.table[num91, (int)Math.Round(num90 + (double)tb.table_y / 2.0)] = tb.table[1, (int)Math.Round(num90 + (double)tb.table_y / 2.0)];
							}
						}
					}
					switch (b)
					{
					case 2:
						tb.nm = "WOT " + tb.nm;
						tb.table_x = 1;
						tb.xaxis[0] = "Speed";
						tb.xunits = "";
						break;
					case 3:
						tb.nm = "WOT " + tb.nm;
						tb.table_x = 2;
						tb.xaxis[0] = "0";
						tb.xaxis[1] = "100";
						tb.xunits = "%";
						break;
					}
				}
				else if (unchecked(ET == 4 || ET == 5 || ET == 102))
				{
					tb.nm += " TUTD";
					int table_y3 = tb.table_y;
					for (int num92 = 1; num92 <= table_y3; num92++)
					{
						int table_x30 = tb.table_x;
						for (int num93 = 1; num93 <= table_x30; num93++)
						{
							if (!CheckBox8.Checked)
							{
								tb.table[num93, num92] = 8192f;
							}
						}
					}
				}
				else if (unchecked(ET == 6 || ET == 25 || ET == 19 || ET == 20 || ET == 103))
				{
					tb.nm += " TUTD";
					int table_y4 = tb.table_y;
					for (int num94 = 1; num94 <= table_y4; num94++)
					{
						int table_x31 = tb.table_x;
						for (int num95 = 2; num95 <= table_x31; num95++)
						{
							if (tb.table[num95 - 1, num94] < tb.table[num95, num94])
							{
								tb.table[num95, num94] = tb.table[num95 - 1, num94];
							}
						}
					}
				}
			}
			if (tb.v != 1)
			{
				return;
			}
			if ((Split == 1) & (tb.table_y > 1))
			{
				tb.table_y = (int)Math.Round((double)tb.table_y / 2.0);
			}
			if ((Split == 2) & (tb.table_y > 1))
			{
				double num96 = (double)tb.table_y / 2.0;
				for (double num97 = 1.0; num97 <= num96; num97 += 1.0)
				{
					int table_x32 = tb.table_x;
					for (int num98 = 1; num98 <= table_x32; num98++)
					{
						tb.table[num98, (int)Math.Round(num97)] = tb.table[num98, (int)Math.Round(num97 + (double)tb.table_y / 2.0)];
					}
					tb.yaxis[(int)Math.Round(num97 - 1.0)] = tb.yaxis[(int)Math.Round(num97 - 1.0 + (double)tb.table_y / 2.0)];
				}
				tb.table_y = (int)Math.Round((double)tb.table_y / 2.0);
			}
			if (tb.tn == 0)
			{
				table_disp(ref tb);
			}
			else
			{
				table_out(ref TempFile, ref tb);
			}
		}
	}

	public void EF(object sender, EventArgs e)
	{
		//IL_0057: Unknown result type (might be due to invalid IL or missing references)
		//IL_005d: Invalid comparison between Unknown and I4
		if (!((ComboBox1.SelectedIndex >= 1) | (ComboBox1.SelectedIndex <= 4)))
		{
			return;
		}
		if (Operators.CompareString(((FileDialog)SaveFileDialog1).FileName, "", false) == 0)
		{
			((FileDialog)SaveFileDialog1).FileName = "Trans_Export.htt";
		}
		if ((int)((CommonDialog)SaveFileDialog1).ShowDialog() != 1)
		{
			return;
		}
		int num = 0;
		int num2 = 0;
		uint num3 = 0u;
		uint num4 = 0u;
		if (File.Exists(((FileDialog)SaveFileDialog1).FileName))
		{
			File.Delete(((FileDialog)SaveFileDialog1).FileName);
		}
		FileStream TempFile = new FileStream(((FileDialog)SaveFileDialog1).FileName, FileMode.OpenOrCreate, FileAccess.ReadWrite);
		int num5 = 0 - (MyProject.Forms.Main_Form.Metric.Checked ? 1 : 0);
		MyProject.Forms.Main_Form.Metric.Checked = false;
		Update_VSS();
		w_string(ref TempFile, "HPT R");
		w_byte(ref TempFile, 1);
		int num6 = 1;
		checked
		{
			do
			{
				w_byte(ref TempFile, 0);
				num6++;
			}
			while (num6 <= 16);
			num3 = (uint)TempFile.Position;
			w_lsb_int(ref TempFile, 0);
			if (CheckBox2.Checked)
			{
				if ((ComboBox2.SelectedIndex == 2) | (ComboBox2.SelectedIndex == 3))
				{
					c_out(ref TempFile, 9000, Conversion.Val(TextBox1.Text), 87);
					num++;
					if (CheckBox20.Checked)
					{
						c_out(ref TempFile, 5001, Conversion.Val(TextBox2.Text), 150);
						num++;
					}
					c_out(ref TempFile, 9050, Conversion.Val(TextBox3.Text), 0);
					num++;
					c_out(ref TempFile, 5002, Conversion.Val(TextBox4.Text), 87);
					num++;
				}
				else if (ComboBox2.SelectedIndex >= 4)
				{
					if (CheckBox20.Checked)
					{
						c_out(ref TempFile, 5001, Conversion.Val(TextBox1.Text), 150);
						num++;
					}
					if (CheckBox20.Checked)
					{
						c_out(ref TempFile, 9002, Conversion.Val(TextBox1.Text), 150);
						num++;
					}
					double num7 = Conversion.Val(TextBox2.Text);
					double c = num7;
					double c2 = num7;
					if (CheckBox15.Checked & (ComboBox1.SelectedIndex >= 3))
					{
						c = num7 / 1.609;
					}
					if (CheckBox16.Checked & (ComboBox1.SelectedIndex >= 3))
					{
						c2 = num7 / 1.609;
					}
					c_out(ref TempFile, 5006, c2, 87);
					num++;
					c_out(ref TempFile, 5007, c2, 87);
					num++;
					c_out(ref TempFile, 9003, c, 87);
					num++;
					c_out(ref TempFile, 9004, c, 87);
					num++;
					c_out(ref TempFile, 5004, Conversion.Val(TextBox3.Text), 0);
					num++;
					if (ComboBox2.SelectedIndex == 5)
					{
						c_out(ref TempFile, 5005, Convert.ToDouble(MyProject.Forms.Main_Form.Gear.Value), 0);
						num++;
					}
					else
					{
						c_out(ref TempFile, 5005, Conversion.Val(TextBox3.Text), 0);
						num++;
					}
					c_out(ref TempFile, 9050, Conversion.Val(TextBox3.Text), 0);
					num++;
					c_out(ref TempFile, 9052, Conversion.Val(TextBox3.Text), 0);
					num++;
					c_out(ref TempFile, 9054, Conversion.Val(TextBox4.Text), 199);
					num++;
					c_out(ref TempFile, 9056, Conversion.Val(TextBox5.Text), 199);
					num++;
				}
			}
			if (((ComboBox1.SelectedIndex == 1) | (ComboBox1.SelectedIndex == 2)) & CheckBox19.Checked)
			{
				int num8 = Convert.ToInt32(MyProject.Forms.Main_Form.Gears.Value);
				double num9 = MyProject.Forms.Main_Form.Ratio.R_Data(1, (byte)num8);
				double num10 = Convert.ToDouble(MyProject.Forms.Main_Form.Gear.Value);
				double num11 = Convert.ToDouble(MyProject.Forms.Main_Form.Tire.Value);
				double num12 = Convert.ToDouble(MyProject.Forms.TCC_Form.MinTCCrpm.Value);
				double num13 = num12 / (num9 * num10) * (num11 * 3.14) * 60.0 / 12.0 / 5280.0;
				if ((decimal.Compare(MyProject.Forms.TCC_Form.MinTCCmintps.Value, 0m) == 0) & (decimal.Compare(MyProject.Forms.TCC_Form.MinTCCmaxtps.Value, 0m) == 0))
				{
					c_out(ref TempFile, 5680, Conversions.ToDouble(MyProject.Forms.Main_Form.Dis_Low), 150);
					num++;
					c_out(ref TempFile, 5681, Conversions.ToDouble(MyProject.Forms.Main_Form.Dis_High), 150);
					num++;
				}
				else
				{
					c_out(ref TempFile, 5680, num13, 150);
					num++;
					c_out(ref TempFile, 5681, num13 + Conversion.Val(((ToolStripControlHost)MyProject.Forms.Main_Form.Lock_Spread).Text), 150);
					num++;
				}
				c_out(ref TempFile, 5682, Convert.ToDouble(MyProject.Forms.TCC_Form.MinTCCmintps.Value), 156);
				num++;
				c_out(ref TempFile, 5683, Convert.ToDouble(MyProject.Forms.TCC_Form.MinTCCmaxtps.Value), 156);
				num++;
				c_out(ref TempFile, 5684, 0.0, 156);
				num++;
				c_out(ref TempFile, 5685, 0.0, 156);
				num++;
			}
			if (CheckBox13.Checked)
			{
				if (ComboBox1.SelectedIndex == 1)
				{
					c_out(ref TempFile, 3035, Convert.ToDouble(Gear.Value), 150);
					num++;
				}
				else if ((ComboBox1.SelectedIndex >= 2) & (ComboBox1.SelectedIndex <= 4))
				{
					c_out(ref TempFile, 9076, Convert.ToDouble(Gear.Value), 150);
					num++;
				}
			}
			num4 = (uint)TempFile.Position;
			TempFile.Position = num3;
			w_lsb_int(ref TempFile, (ushort)num);
			TempFile.Position = num4;
			num3 = (uint)TempFile.Position;
			w_lsb_int(ref TempFile, 0);
			if (ComboBox1.SelectedIndex == 1)
			{
				if (CheckBox4.Checked)
				{
					Gen_Table(1, 15000, 0, ref TempFile);
					num2++;
					Gen_Table(2, 15010, 0, ref TempFile);
					num2++;
					Gen_Table(4, 15020, 0, ref TempFile);
					num2++;
					Gen_Table(6, 15200, 0, ref TempFile);
					num2++;
					Gen_Table(7, 15205, 0, ref TempFile);
					num2++;
					if (CheckBox10.Checked)
					{
						Gen_Table(28, 15300, 0, ref TempFile);
						num2++;
						Gen_Table(29, 15357, 0, ref TempFile);
						num2++;
						Gen_Table(30, 15329, 1, ref TempFile);
						num2++;
						Gen_Table(30, 15331, 2, ref TempFile);
						num2++;
						Gen_Table(31, 15330, 1, ref TempFile);
						num2++;
						Gen_Table(31, 15332, 2, ref TempFile);
						num2++;
						Gen_Table(32, 15210, 0, ref TempFile);
						num2++;
					}
				}
				if (CheckBox5.Checked)
				{
					Apply_Mode_Mutate(ComboBox3.SelectedIndex);
					Gen_Table(1, 15003, 0, ref TempFile);
					num2++;
					Gen_Table(2, 15013, 0, ref TempFile);
					num2++;
					Gen_Table(4, 15023, 0, ref TempFile);
					num2++;
					Gen_Table(6, 15203, 0, ref TempFile);
					num2++;
					if (CheckBox10.Checked)
					{
						Gen_Table(32, 15213, 0, ref TempFile);
						num2++;
					}
					Revert_Mode_Mutate();
				}
				if (CheckBox6.Checked)
				{
					Apply_Mode_Mutate(ComboBox4.SelectedIndex);
					Gen_Table(1, 15001, 0, ref TempFile);
					num2++;
					Gen_Table(6, 15201, 0, ref TempFile);
					num2++;
					if (CheckBox10.Checked)
					{
						Gen_Table(32, 15211, 0, ref TempFile);
						num2++;
					}
					Revert_Mode_Mutate();
				}
				if (CheckBox7.Checked)
				{
					Gen_Table(1, 15002, 0, ref TempFile);
					num2++;
					Gen_Table(2, 15012, 0, ref TempFile);
					num2++;
					Gen_Table(4, 15022, 0, ref TempFile);
					num2++;
					Gen_Table(6, 15202, 0, ref TempFile);
					num2++;
					Gen_Table(7, 15206, 0, ref TempFile);
					num2++;
				}
				if (CheckBox13.Checked)
				{
					Apply_Mode_Mutate(10);
					Gen_Table(2, 14998, 0, ref TempFile);
					num2++;
					Gen_Table(4, 14999, 0, ref TempFile);
					num2++;
					Revert_Mode_Mutate();
				}
			}
			else if (ComboBox1.SelectedIndex == 2)
			{
				int eT = ((!CheckBox1.Checked) ? 2 : 3);
				int eT2 = ((!CheckBox1.Checked) ? 4 : 5);
				int eT3 = ((!CheckBox1.Checked) ? 7 : 8);
				if (CheckBox4.Checked)
				{
					Gen_Table(1, 15000, 0, ref TempFile);
					num2++;
					Gen_Table(eT, 15010, 0, ref TempFile);
					num2++;
					Gen_Table(eT2, 15020, 0, ref TempFile);
					num2++;
					Gen_Table(6, 15200, 0, ref TempFile);
					num2++;
					Gen_Table(eT3, 15205, 0, ref TempFile);
					num2++;
					if (CheckBox10.Checked)
					{
						Gen_Table(33, 15300, 0, ref TempFile);
						num2++;
						Gen_Table(30, 15301, 0, ref TempFile);
						num2++;
						Gen_Table(35, 15247, 0, ref TempFile);
						num2++;
						Gen_Table(34, 15246, 0, ref TempFile);
						num2++;
					}
				}
				if (CheckBox5.Checked)
				{
					Apply_Mode_Mutate(ComboBox3.SelectedIndex);
					Gen_Table(1, 15315, 0, ref TempFile);
					num2++;
					Gen_Table(eT, 15323, 0, ref TempFile);
					num2++;
					Gen_Table(eT2, 15090, 0, ref TempFile);
					num2++;
					Gen_Table(6, 15285, 0, ref TempFile);
					num2++;
					Gen_Table(eT3, 15293, 0, ref TempFile);
					num2++;
					if (CheckBox10.Checked)
					{
						Gen_Table(30, 15318, 0, ref TempFile);
						num2++;
						Gen_Table(34, 15288, 0, ref TempFile);
						num2++;
					}
					Revert_Mode_Mutate();
				}
				if (CheckBox6.Checked)
				{
					Apply_Mode_Mutate(ComboBox4.SelectedIndex);
					Gen_Table(1, 15319, 0, ref TempFile);
					num2++;
					Gen_Table(eT, 15326, 0, ref TempFile);
					num2++;
					Gen_Table(eT2, 15093, 0, ref TempFile);
					num2++;
					Gen_Table(6, 15289, 0, ref TempFile);
					num2++;
					Gen_Table(eT3, 15296, 0, ref TempFile);
					num2++;
					if (CheckBox10.Checked)
					{
						Gen_Table(30, 15322, 0, ref TempFile);
						num2++;
						Gen_Table(34, 15292, 0, ref TempFile);
						num2++;
					}
					Revert_Mode_Mutate();
				}
				if (CheckBox7.Checked)
				{
					Gen_Table(1, 15002, 0, ref TempFile);
					num2++;
					Gen_Table(eT, 15012, 0, ref TempFile);
					num2++;
					Gen_Table(eT, 15017, 0, ref TempFile);
					num2++;
					Gen_Table(eT2, 15022, 0, ref TempFile);
					num2++;
					Gen_Table(eT2, 15027, 0, ref TempFile);
					num2++;
					Gen_Table(6, 15202, 0, ref TempFile);
					num2++;
					Gen_Table(eT3, 15206, 0, ref TempFile);
					num2++;
					Gen_Table(eT3, 15267, 0, ref TempFile);
					num2++;
					if (CheckBox10.Checked)
					{
						Gen_Table(30, 15303, 0, ref TempFile);
						num2++;
						Gen_Table(34, 15249, 0, ref TempFile);
						num2++;
					}
				}
				if (CheckBox3.Checked)
				{
					Gen_Table(37, 15004, 0, ref TempFile);
					num2++;
					Gen_Table(38, 15005, 0, ref TempFile);
					num2++;
					Gen_Table(52, 15240, 1, ref TempFile);
					num2++;
					Gen_Table(52, 15241, 2, ref TempFile);
					num2++;
					Gen_Table(52, 15244, 1, ref TempFile);
					num2++;
					Gen_Table(52, 15245, 2, ref TempFile);
					num2++;
				}
				if (CheckBox9.Checked)
				{
					if (CheckBox1.Checked)
					{
						Gen_Table(54, 15305, 0, ref TempFile);
						num2++;
						Gen_Table(54, 15306, 0, ref TempFile);
						num2++;
						Gen_Table(62, 15307, 0, ref TempFile);
						num2++;
					}
					else
					{
						Gen_Table(53, 15305, 0, ref TempFile);
						num2++;
						Gen_Table(53, 15306, 0, ref TempFile);
						num2++;
						Gen_Table(61, 15307, 0, ref TempFile);
						num2++;
					}
				}
			}
			else if (ComboBox1.SelectedIndex == 3)
			{
				int eT4;
				int eT5;
				int eT6;
				int eT7;
				int eT8;
				int eT9;
				int eT10;
				int eT11;
				int eT12;
				if (CheckBox1.Checked)
				{
					eT4 = 3;
					eT5 = 12;
					eT6 = 14;
					eT7 = 5;
					eT8 = 16;
					eT9 = 18;
					eT10 = 27;
					eT11 = 22;
					eT12 = 24;
				}
				else
				{
					eT4 = 2;
					eT5 = 11;
					eT6 = 13;
					eT7 = 4;
					eT8 = 15;
					eT9 = 17;
					eT10 = 26;
					eT11 = 21;
					eT12 = 23;
				}
				if (CheckBox4.Checked)
				{
					Gen_Table(1, 15000, 0, ref TempFile);
					num2++;
					Gen_Table(9, 15050, 0, ref TempFile);
					num2++;
					Gen_Table(10, 15051, 0, ref TempFile);
					num2++;
					Gen_Table(eT4, 15010, 0, ref TempFile);
					num2++;
					Gen_Table(eT5, 15064, 0, ref TempFile);
					num2++;
					Gen_Table(eT6, 15065, 0, ref TempFile);
					num2++;
					Gen_Table(eT7, 15020, 0, ref TempFile);
					num2++;
					Gen_Table(eT8, 15080, 0, ref TempFile);
					num2++;
					Gen_Table(eT9, 15081, 0, ref TempFile);
					num2++;
					Gen_Table(25, 15200, 0, ref TempFile);
					num2++;
					Gen_Table(19, 15251, 0, ref TempFile);
					num2++;
					Gen_Table(20, 15252, 0, ref TempFile);
					num2++;
					Gen_Table(eT10, 15205, 0, ref TempFile);
					num2++;
					Gen_Table(eT11, 15270, 0, ref TempFile);
					num2++;
					Gen_Table(eT12, 15271, 0, ref TempFile);
					num2++;
					if (CheckBox10.Checked)
					{
						Gen_Table(33, 15300, 0, ref TempFile);
						num2++;
						Gen_Table(30, 15301, 0, ref TempFile);
						num2++;
						Gen_Table(36, 15247, 0, ref TempFile);
						num2++;
						Gen_Table(36, 15246, 0, ref TempFile);
						num2++;
					}
				}
				if (CheckBox5.Checked)
				{
					Apply_Mode_Mutate(ComboBox3.SelectedIndex);
					Gen_Table(1, 15315, 0, ref TempFile);
					num2++;
					Gen_Table(9, 15316, 0, ref TempFile);
					num2++;
					Gen_Table(10, 15317, 0, ref TempFile);
					num2++;
					Gen_Table(eT4, 15323, 0, ref TempFile);
					num2++;
					Gen_Table(eT5, 15324, 0, ref TempFile);
					num2++;
					Gen_Table(eT6, 15325, 0, ref TempFile);
					num2++;
					Gen_Table(eT7, 15090, 0, ref TempFile);
					num2++;
					Gen_Table(eT8, 15091, 0, ref TempFile);
					num2++;
					Gen_Table(eT9, 15092, 0, ref TempFile);
					num2++;
					Gen_Table(25, 15285, 0, ref TempFile);
					num2++;
					Gen_Table(19, 15286, 0, ref TempFile);
					num2++;
					Gen_Table(20, 15287, 0, ref TempFile);
					num2++;
					Gen_Table(eT10, 15293, 0, ref TempFile);
					num2++;
					Gen_Table(eT11, 15294, 0, ref TempFile);
					num2++;
					Gen_Table(eT12, 15295, 0, ref TempFile);
					num2++;
					if (CheckBox10.Checked)
					{
						Gen_Table(30, 15318, 0, ref TempFile);
						num2++;
						Gen_Table(36, 15288, 0, ref TempFile);
						num2++;
					}
					Revert_Mode_Mutate();
				}
				if (CheckBox6.Checked)
				{
					Apply_Mode_Mutate(ComboBox4.SelectedIndex);
					Gen_Table(1, 15319, 0, ref TempFile);
					num2++;
					Gen_Table(9, 15320, 0, ref TempFile);
					num2++;
					Gen_Table(10, 15321, 0, ref TempFile);
					num2++;
					Gen_Table(eT4, 15326, 0, ref TempFile);
					num2++;
					Gen_Table(eT5, 15327, 0, ref TempFile);
					num2++;
					Gen_Table(eT6, 15328, 0, ref TempFile);
					num2++;
					Gen_Table(eT7, 15093, 0, ref TempFile);
					num2++;
					Gen_Table(eT8, 15094, 0, ref TempFile);
					num2++;
					Gen_Table(eT9, 15095, 0, ref TempFile);
					num2++;
					Gen_Table(25, 15289, 0, ref TempFile);
					num2++;
					Gen_Table(19, 15290, 0, ref TempFile);
					num2++;
					Gen_Table(20, 15291, 0, ref TempFile);
					num2++;
					Gen_Table(eT10, 15296, 0, ref TempFile);
					num2++;
					Gen_Table(eT11, 15297, 0, ref TempFile);
					num2++;
					Gen_Table(eT12, 15298, 0, ref TempFile);
					num2++;
					if (CheckBox10.Checked)
					{
						Gen_Table(30, 15322, 0, ref TempFile);
						num2++;
						Gen_Table(36, 15292, 0, ref TempFile);
						num2++;
					}
					Revert_Mode_Mutate();
				}
				if (CheckBox7.Checked)
				{
					Gen_Table(1, 15002, 0, ref TempFile);
					num2++;
					Gen_Table(9, 15054, 0, ref TempFile);
					num2++;
					Gen_Table(10, 15055, 0, ref TempFile);
					num2++;
					Gen_Table(eT4, 15012, 0, ref TempFile);
					num2++;
					Gen_Table(eT4, 15017, 0, ref TempFile);
					num2++;
					Gen_Table(eT5, 15068, 0, ref TempFile);
					num2++;
					Gen_Table(eT5, 15076, 0, ref TempFile);
					num2++;
					Gen_Table(eT6, 15069, 0, ref TempFile);
					num2++;
					Gen_Table(eT6, 15077, 0, ref TempFile);
					num2++;
					Gen_Table(eT7, 15022, 0, ref TempFile);
					num2++;
					Gen_Table(eT7, 15027, 0, ref TempFile);
					num2++;
					Gen_Table(eT8, 15084, 0, ref TempFile);
					num2++;
					Gen_Table(eT8, 15088, 0, ref TempFile);
					num2++;
					Gen_Table(eT9, 15085, 0, ref TempFile);
					num2++;
					Gen_Table(eT9, 15089, 0, ref TempFile);
					num2++;
					Gen_Table(25, 15242, 1, ref TempFile);
					num2++;
					Gen_Table(25, 15243, 2, ref TempFile);
					num2++;
					Gen_Table(19, 15255, 1, ref TempFile);
					num2++;
					Gen_Table(19, 15257, 2, ref TempFile);
					num2++;
					Gen_Table(20, 15256, 1, ref TempFile);
					num2++;
					Gen_Table(20, 15258, 2, ref TempFile);
					num2++;
					Gen_Table(eT10, 15206, 0, ref TempFile);
					num2++;
					Gen_Table(eT10, 15267, 0, ref TempFile);
					num2++;
					Gen_Table(eT11, 15274, 0, ref TempFile);
					num2++;
					Gen_Table(eT11, 15278, 0, ref TempFile);
					num2++;
					Gen_Table(eT12, 15275, 0, ref TempFile);
					num2++;
					Gen_Table(eT12, 15279, 0, ref TempFile);
					num2++;
					if (CheckBox10.Checked)
					{
						Gen_Table(30, 15303, 0, ref TempFile);
						num2++;
						Gen_Table(36, 15249, 0, ref TempFile);
						num2++;
					}
				}
				if (CheckBox3.Checked)
				{
					Gen_Table(37, 15004, 0, ref TempFile);
					num2++;
					Gen_Table(38, 15005, 0, ref TempFile);
					num2++;
					Gen_Table(38, 15006, 2, ref TempFile);
					num2++;
					Gen_Table(39, 15058, 0, ref TempFile);
					num2++;
					Gen_Table(39, 15060, 0, ref TempFile);
					num2++;
					Gen_Table(39, 15062, 2, ref TempFile);
					num2++;
					Gen_Table(40, 15059, 0, ref TempFile);
					num2++;
					Gen_Table(40, 15061, 0, ref TempFile);
					num2++;
					Gen_Table(40, 15063, 2, ref TempFile);
					num2++;
					if (CheckBox1.Checked)
					{
						Gen_Table(42, 15015, 0, ref TempFile);
						num2++;
						Gen_Table(44, 15074, 0, ref TempFile);
						num2++;
						Gen_Table(46, 15075, 0, ref TempFile);
						num2++;
						Gen_Table(48, 15025, 0, ref TempFile);
						num2++;
					}
					else
					{
						Gen_Table(41, 15015, 0, ref TempFile);
						num2++;
						Gen_Table(43, 15074, 0, ref TempFile);
						num2++;
						Gen_Table(45, 15075, 0, ref TempFile);
						num2++;
						Gen_Table(47, 15025, 0, ref TempFile);
						num2++;
					}
					Gen_Table(49, 15240, 1, ref TempFile);
					num2++;
					Gen_Table(49, 15241, 2, ref TempFile);
					num2++;
					Gen_Table(49, 15244, 1, ref TempFile);
					num2++;
					Gen_Table(49, 15245, 2, ref TempFile);
					num2++;
					Gen_Table(50, 15261, 0, ref TempFile);
					num2++;
					Gen_Table(50, 15263, 1, ref TempFile);
					num2++;
					Gen_Table(50, 15265, 2, ref TempFile);
					num2++;
					Gen_Table(51, 15262, 0, ref TempFile);
					num2++;
					Gen_Table(51, 15264, 1, ref TempFile);
					num2++;
					Gen_Table(51, 15266, 2, ref TempFile);
					num2++;
				}
				if (CheckBox9.Checked)
				{
					if (CheckBox1.Checked)
					{
						Gen_Table(54, 15305, 0, ref TempFile);
						num2++;
						Gen_Table(54, 15306, 0, ref TempFile);
						num2++;
						Gen_Table(62, 15307, 0, ref TempFile);
						num2++;
						Gen_Table(56, 15308, 0, ref TempFile);
						num2++;
						Gen_Table(56, 15310, 0, ref TempFile);
						num2++;
						Gen_Table(58, 15309, 0, ref TempFile);
						num2++;
						Gen_Table(58, 15311, 0, ref TempFile);
						num2++;
					}
					else
					{
						Gen_Table(53, 15305, 0, ref TempFile);
						num2++;
						Gen_Table(53, 15306, 0, ref TempFile);
						num2++;
						Gen_Table(61, 15307, 0, ref TempFile);
						num2++;
						Gen_Table(55, 15308, 0, ref TempFile);
						num2++;
						Gen_Table(55, 15310, 0, ref TempFile);
						num2++;
						Gen_Table(57, 15309, 0, ref TempFile);
						num2++;
						Gen_Table(57, 15311, 0, ref TempFile);
						num2++;
					}
					if (CheckBox14.Checked)
					{
						Gen_Table(59, 15312, 0, ref TempFile);
						num2++;
						Gen_Table(60, 15313, 0, ref TempFile);
						num2++;
					}
					else
					{
						Gen_Table(9, 15312, 0, ref TempFile);
						num2++;
						Gen_Table(10, 15313, 0, ref TempFile);
						num2++;
					}
				}
				if (CheckBox13.Checked)
				{
					Apply_Mode_Mutate(10);
					Gen_Table(2, 15014, 0, ref TempFile);
					num2++;
					Gen_Table(11, 15072, 0, ref TempFile);
					num2++;
					Gen_Table(13, 15073, 0, ref TempFile);
					num2++;
					Gen_Table(4, 15024, 0, ref TempFile);
					num2++;
					Gen_Table(26, 15269, 0, ref TempFile);
					num2++;
					Gen_Table(21, 15280, 0, ref TempFile);
					num2++;
					Gen_Table(23, 15281, 0, ref TempFile);
					num2++;
					Revert_Mode_Mutate();
				}
			}
			else if (ComboBox1.SelectedIndex == 4)
			{
				int eT13;
				int eT14;
				int eT15;
				int eT16;
				int eT17;
				int eT18;
				int eT19;
				int eT20;
				int eT21;
				if (CheckBox1.Checked)
				{
					eT13 = 3;
					eT14 = 12;
					eT15 = 14;
					eT16 = 5;
					eT17 = 16;
					eT18 = 18;
					eT19 = 27;
					eT20 = 22;
					eT21 = 24;
				}
				else
				{
					eT13 = 2;
					eT14 = 11;
					eT15 = 13;
					eT16 = 4;
					eT17 = 15;
					eT18 = 17;
					eT19 = 26;
					eT20 = 21;
					eT21 = 23;
				}
				if (CheckBox4.Checked)
				{
					Gen_Table(1, 15028, 1, ref TempFile);
					num2++;
					Gen_Table(1, 15034, 2, ref TempFile);
					num2++;
					Gen_Table(9, 15337, 1, ref TempFile);
					num2++;
					Gen_Table(9, 15338, 2, ref TempFile);
					num2++;
					Gen_Table(10, 15349, 1, ref TempFile);
					num2++;
					Gen_Table(10, 15350, 2, ref TempFile);
					num2++;
					Gen_Table(eT13, 15010, 0, ref TempFile);
					num2++;
					Gen_Table(eT14, 15064, 0, ref TempFile);
					num2++;
					Gen_Table(eT15, 15065, 0, ref TempFile);
					num2++;
					Gen_Table(eT16, 15020, 0, ref TempFile);
					num2++;
					Gen_Table(eT17, 15080, 0, ref TempFile);
					num2++;
					Gen_Table(eT18, 15081, 0, ref TempFile);
					num2++;
					Gen_Table(25, 15223, 1, ref TempFile);
					num2++;
					Gen_Table(25, 15224, 2, ref TempFile);
					num2++;
					Gen_Table(19, 15217, 1, ref TempFile);
					num2++;
					Gen_Table(19, 15218, 2, ref TempFile);
					num2++;
					Gen_Table(20, 15252, 0, ref TempFile);
					num2++;
					Gen_Table(eT19, 15205, 0, ref TempFile);
					num2++;
					Gen_Table(eT20, 15270, 0, ref TempFile);
					num2++;
					Gen_Table(eT21, 15271, 0, ref TempFile);
					num2++;
					if (CheckBox10.Checked)
					{
						Gen_Table(33, 15300, 0, ref TempFile);
						num2++;
						Gen_Table(30, 15301, 0, ref TempFile);
						num2++;
						Gen_Table(36, 15247, 0, ref TempFile);
						num2++;
						Gen_Table(36, 15246, 0, ref TempFile);
						num2++;
					}
				}
				if (CheckBox5.Checked)
				{
					Apply_Mode_Mutate(ComboBox3.SelectedIndex);
					Gen_Table(1, 15030, 1, ref TempFile);
					num2++;
					Gen_Table(1, 15036, 2, ref TempFile);
					num2++;
					Gen_Table(9, 15341, 1, ref TempFile);
					num2++;
					Gen_Table(9, 15342, 2, ref TempFile);
					num2++;
					Gen_Table(10, 15353, 1, ref TempFile);
					num2++;
					Gen_Table(10, 15354, 2, ref TempFile);
					num2++;
					Gen_Table(eT13, 15323, 0, ref TempFile);
					num2++;
					Gen_Table(eT14, 15324, 0, ref TempFile);
					num2++;
					Gen_Table(eT15, 15325, 0, ref TempFile);
					num2++;
					Gen_Table(eT16, 15090, 0, ref TempFile);
					num2++;
					Gen_Table(eT17, 15091, 0, ref TempFile);
					num2++;
					Gen_Table(eT18, 15092, 0, ref TempFile);
					num2++;
					Gen_Table(25, 15225, 1, ref TempFile);
					num2++;
					Gen_Table(25, 15226, 2, ref TempFile);
					num2++;
					Gen_Table(19, 15219, 1, ref TempFile);
					num2++;
					Gen_Table(19, 15220, 2, ref TempFile);
					num2++;
					Gen_Table(20, 15287, 0, ref TempFile);
					num2++;
					Gen_Table(eT19, 15293, 0, ref TempFile);
					num2++;
					Gen_Table(eT20, 15294, 0, ref TempFile);
					num2++;
					Gen_Table(eT21, 15295, 0, ref TempFile);
					num2++;
					if (CheckBox10.Checked)
					{
						Gen_Table(30, 15318, 0, ref TempFile);
						num2++;
						Gen_Table(36, 15288, 0, ref TempFile);
						num2++;
					}
					Revert_Mode_Mutate();
				}
				if (CheckBox6.Checked)
				{
					Apply_Mode_Mutate(ComboBox4.SelectedIndex);
					Gen_Table(1, 15031, 1, ref TempFile);
					num2++;
					Gen_Table(1, 15037, 2, ref TempFile);
					num2++;
					Gen_Table(9, 15343, 1, ref TempFile);
					num2++;
					Gen_Table(9, 15344, 2, ref TempFile);
					num2++;
					Gen_Table(10, 15355, 1, ref TempFile);
					num2++;
					Gen_Table(10, 15356, 2, ref TempFile);
					num2++;
					Gen_Table(eT13, 15326, 0, ref TempFile);
					num2++;
					Gen_Table(eT14, 15327, 0, ref TempFile);
					num2++;
					Gen_Table(eT15, 15328, 0, ref TempFile);
					num2++;
					Gen_Table(eT16, 15093, 0, ref TempFile);
					num2++;
					Gen_Table(eT17, 15094, 0, ref TempFile);
					num2++;
					Gen_Table(eT18, 15095, 0, ref TempFile);
					num2++;
					Gen_Table(25, 15227, 1, ref TempFile);
					num2++;
					Gen_Table(25, 15228, 2, ref TempFile);
					num2++;
					Gen_Table(19, 15221, 1, ref TempFile);
					num2++;
					Gen_Table(19, 15229, 2, ref TempFile);
					num2++;
					Gen_Table(20, 15291, 0, ref TempFile);
					num2++;
					Gen_Table(eT19, 15296, 0, ref TempFile);
					num2++;
					Gen_Table(eT20, 15297, 0, ref TempFile);
					num2++;
					Gen_Table(eT21, 15298, 0, ref TempFile);
					num2++;
					if (CheckBox10.Checked)
					{
						Gen_Table(30, 15322, 0, ref TempFile);
						num2++;
						Gen_Table(36, 15292, 0, ref TempFile);
						num2++;
					}
					Revert_Mode_Mutate();
				}
				if (CheckBox7.Checked)
				{
					Gen_Table(1, 15029, 1, ref TempFile);
					num2++;
					Gen_Table(1, 15035, 2, ref TempFile);
					num2++;
					Gen_Table(9, 15339, 1, ref TempFile);
					num2++;
					Gen_Table(9, 15340, 2, ref TempFile);
					num2++;
					Gen_Table(10, 15351, 1, ref TempFile);
					num2++;
					Gen_Table(10, 15352, 2, ref TempFile);
					num2++;
					Gen_Table(eT13, 15012, 0, ref TempFile);
					num2++;
					Gen_Table(eT13, 15017, 0, ref TempFile);
					num2++;
					Gen_Table(eT14, 15068, 0, ref TempFile);
					num2++;
					Gen_Table(eT14, 15076, 0, ref TempFile);
					num2++;
					Gen_Table(eT15, 15069, 0, ref TempFile);
					num2++;
					Gen_Table(eT15, 15077, 0, ref TempFile);
					num2++;
					Gen_Table(eT16, 15022, 0, ref TempFile);
					num2++;
					Gen_Table(eT16, 15027, 0, ref TempFile);
					num2++;
					Gen_Table(eT17, 15084, 0, ref TempFile);
					num2++;
					Gen_Table(eT17, 15088, 0, ref TempFile);
					num2++;
					Gen_Table(eT18, 15085, 0, ref TempFile);
					num2++;
					Gen_Table(eT18, 15089, 0, ref TempFile);
					num2++;
					Gen_Table(25, 15242, 1, ref TempFile);
					num2++;
					Gen_Table(25, 15243, 2, ref TempFile);
					num2++;
					Gen_Table(19, 15255, 1, ref TempFile);
					num2++;
					Gen_Table(19, 15257, 2, ref TempFile);
					num2++;
					Gen_Table(20, 15256, 1, ref TempFile);
					num2++;
					Gen_Table(20, 15258, 2, ref TempFile);
					num2++;
					Gen_Table(eT19, 15206, 0, ref TempFile);
					num2++;
					Gen_Table(eT19, 15267, 0, ref TempFile);
					num2++;
					Gen_Table(eT20, 15274, 0, ref TempFile);
					num2++;
					Gen_Table(eT20, 15278, 0, ref TempFile);
					num2++;
					Gen_Table(eT21, 15275, 0, ref TempFile);
					num2++;
					Gen_Table(eT21, 15279, 0, ref TempFile);
					num2++;
					if (CheckBox10.Checked)
					{
						Gen_Table(30, 15303, 0, ref TempFile);
						num2++;
						Gen_Table(36, 15249, 0, ref TempFile);
						num2++;
					}
				}
				if (CheckBox3.Checked)
				{
					Gen_Table(38, 15033, 1, ref TempFile);
					num2++;
					Gen_Table(38, 15039, 2, ref TempFile);
					num2++;
					Gen_Table(38, 15032, 1, ref TempFile);
					num2++;
					Gen_Table(38, 15038, 2, ref TempFile);
					num2++;
					Gen_Table(38, 15006, 2, ref TempFile);
					num2++;
					Gen_Table(39, 15333, 1, ref TempFile);
					num2++;
					Gen_Table(39, 15334, 2, ref TempFile);
					num2++;
					Gen_Table(39, 15335, 1, ref TempFile);
					num2++;
					Gen_Table(39, 15336, 2, ref TempFile);
					num2++;
					Gen_Table(39, 15062, 2, ref TempFile);
					num2++;
					Gen_Table(40, 15345, 1, ref TempFile);
					num2++;
					Gen_Table(40, 15346, 2, ref TempFile);
					num2++;
					Gen_Table(40, 15347, 1, ref TempFile);
					num2++;
					Gen_Table(40, 15348, 2, ref TempFile);
					num2++;
					Gen_Table(40, 15063, 2, ref TempFile);
					num2++;
					if (CheckBox1.Checked)
					{
						Gen_Table(42, 15015, 0, ref TempFile);
						num2++;
						Gen_Table(44, 15074, 0, ref TempFile);
						num2++;
						Gen_Table(46, 15075, 0, ref TempFile);
						num2++;
						Gen_Table(48, 15025, 0, ref TempFile);
						num2++;
					}
					else
					{
						Gen_Table(41, 15015, 0, ref TempFile);
						num2++;
						Gen_Table(43, 15074, 0, ref TempFile);
						num2++;
						Gen_Table(45, 15075, 0, ref TempFile);
						num2++;
						Gen_Table(47, 15025, 0, ref TempFile);
						num2++;
					}
					Gen_Table(49, 15240, 1, ref TempFile);
					num2++;
					Gen_Table(49, 15241, 2, ref TempFile);
					num2++;
					Gen_Table(49, 15244, 1, ref TempFile);
					num2++;
					Gen_Table(49, 15245, 2, ref TempFile);
					num2++;
					Gen_Table(50, 15215, 1, ref TempFile);
					num2++;
					Gen_Table(50, 15216, 2, ref TempFile);
					num2++;
					Gen_Table(50, 15263, 1, ref TempFile);
					num2++;
					Gen_Table(50, 15265, 2, ref TempFile);
					num2++;
					Gen_Table(51, 15262, 0, ref TempFile);
					num2++;
					Gen_Table(51, 15264, 1, ref TempFile);
					num2++;
					Gen_Table(51, 15266, 2, ref TempFile);
					num2++;
				}
				if (CheckBox9.Checked)
				{
					if (CheckBox1.Checked)
					{
						Gen_Table(54, 15305, 0, ref TempFile);
						num2++;
						Gen_Table(54, 15306, 0, ref TempFile);
						num2++;
						Gen_Table(62, 15307, 0, ref TempFile);
						num2++;
						Gen_Table(56, 15308, 0, ref TempFile);
						num2++;
						Gen_Table(56, 15310, 0, ref TempFile);
						num2++;
						Gen_Table(58, 15309, 0, ref TempFile);
						num2++;
						Gen_Table(58, 15311, 0, ref TempFile);
						num2++;
					}
					else
					{
						Gen_Table(53, 15305, 0, ref TempFile);
						num2++;
						Gen_Table(53, 15306, 0, ref TempFile);
						num2++;
						Gen_Table(61, 15307, 0, ref TempFile);
						num2++;
						Gen_Table(55, 15308, 0, ref TempFile);
						num2++;
						Gen_Table(55, 15310, 0, ref TempFile);
						num2++;
						Gen_Table(57, 15309, 0, ref TempFile);
						num2++;
						Gen_Table(57, 15311, 0, ref TempFile);
						num2++;
					}
					if (CheckBox14.Checked)
					{
						Gen_Table(59, 15312, 0, ref TempFile);
						num2++;
						Gen_Table(60, 15313, 0, ref TempFile);
						num2++;
					}
					else
					{
						Gen_Table(9, 15312, 0, ref TempFile);
						num2++;
						Gen_Table(10, 15313, 0, ref TempFile);
						num2++;
					}
				}
				if (CheckBox13.Checked)
				{
					Apply_Mode_Mutate(10);
					Gen_Table(2, 15014, 0, ref TempFile);
					num2++;
					Gen_Table(11, 15072, 0, ref TempFile);
					num2++;
					Gen_Table(13, 15073, 0, ref TempFile);
					num2++;
					Gen_Table(4, 15024, 0, ref TempFile);
					num2++;
					Gen_Table(26, 15269, 0, ref TempFile);
					num2++;
					Gen_Table(21, 15280, 0, ref TempFile);
					num2++;
					Gen_Table(23, 15281, 0, ref TempFile);
					num2++;
					Revert_Mode_Mutate();
				}
			}
			else if (ComboBox1.SelectedIndex == 5)
			{
				if (CheckBox4.Checked)
				{
					Gen_Table(100, 15028, 1, ref TempFile);
					num2++;
					Gen_Table(100, 15034, 2, ref TempFile);
					num2++;
					Gen_Table(101, 15010, 0, ref TempFile);
					num2++;
					Gen_Table(102, 15020, 0, ref TempFile);
					num2++;
					Gen_Table(103, 15200, 0, ref TempFile);
					num2++;
					Gen_Table(104, 15205, 0, ref TempFile);
					num2++;
					if (CheckBox10.Checked)
					{
						Gen_Table(105, 15247, 0, ref TempFile);
						num2++;
						Gen_Table(105, 15246, 0, ref TempFile);
						num2++;
						Gen_Table(101, 39433, 0, ref TempFile);
						num2++;
						Gen_Table(101, 39434, 0, ref TempFile);
						num2++;
						Gen_Table(103, 39420, 1, ref TempFile);
						num2++;
						Gen_Table(103, 39419, 2, ref TempFile);
						num2++;
					}
				}
				if (CheckBox5.Checked)
				{
					Apply_Mode_Mutate(ComboBox3.SelectedIndex);
					Gen_Table(100, 15030, 1, ref TempFile);
					num2++;
					Gen_Table(100, 15036, 2, ref TempFile);
					num2++;
					Gen_Table(101, 15323, 0, ref TempFile);
					num2++;
					Gen_Table(102, 15090, 0, ref TempFile);
					num2++;
					Gen_Table(103, 15285, 0, ref TempFile);
					num2++;
					Gen_Table(104, 15293, 0, ref TempFile);
					num2++;
					if (CheckBox10.Checked)
					{
						Gen_Table(105, 15288, 0, ref TempFile);
						num2++;
					}
					Revert_Mode_Mutate();
				}
				if (CheckBox6.Checked)
				{
					Apply_Mode_Mutate(ComboBox4.SelectedIndex);
					Gen_Table(100, 15031, 1, ref TempFile);
					num2++;
					Gen_Table(100, 15037, 2, ref TempFile);
					num2++;
					Gen_Table(101, 15326, 0, ref TempFile);
					num2++;
					Gen_Table(102, 15093, 0, ref TempFile);
					num2++;
					Gen_Table(103, 15289, 0, ref TempFile);
					num2++;
					Gen_Table(104, 15296, 0, ref TempFile);
					num2++;
					if (CheckBox10.Checked)
					{
						Gen_Table(105, 15292, 0, ref TempFile);
						num2++;
					}
					Revert_Mode_Mutate();
				}
				if (CheckBox7.Checked)
				{
					Gen_Table(100, 15029, 1, ref TempFile);
					num2++;
					Gen_Table(100, 15035, 2, ref TempFile);
					num2++;
					Gen_Table(101, 15012, 0, ref TempFile);
					num2++;
					Gen_Table(101, 15017, 0, ref TempFile);
					num2++;
					Gen_Table(102, 15022, 0, ref TempFile);
					num2++;
					Gen_Table(102, 15027, 0, ref TempFile);
					num2++;
					Gen_Table(103, 15202, 0, ref TempFile);
					num2++;
					Gen_Table(104, 15206, 0, ref TempFile);
					num2++;
					Gen_Table(104, 15267, 0, ref TempFile);
					num2++;
					if (CheckBox10.Checked)
					{
						Gen_Table(105, 15249, 0, ref TempFile);
						num2++;
					}
				}
				if (CheckBox3.Checked)
				{
					Gen_Table(138, 15033, 1, ref TempFile);
					num2++;
					Gen_Table(138, 15039, 2, ref TempFile);
					num2++;
					Gen_Table(138, 15032, 1, ref TempFile);
					num2++;
					Gen_Table(138, 15038, 2, ref TempFile);
					num2++;
					Gen_Table(141, 15015, 0, ref TempFile);
					num2++;
					Gen_Table(139, 15025, 0, ref TempFile);
					num2++;
					Gen_Table(140, 15241, 1, ref TempFile);
					num2++;
					Gen_Table(140, 15240, 2, ref TempFile);
					num2++;
					Gen_Table(140, 15245, 1, ref TempFile);
					num2++;
					Gen_Table(140, 15244, 2, ref TempFile);
					num2++;
				}
				if (CheckBox13.Checked)
				{
					Apply_Mode_Mutate(10);
					Gen_Table(100, 39424, 1, ref TempFile);
					num2++;
					Gen_Table(100, 39425, 2, ref TempFile);
					num2++;
					Gen_Table(101, 15014, 0, ref TempFile);
					num2++;
					Gen_Table(102, 15024, 0, ref TempFile);
					num2++;
					Gen_Table(103, 15204, 0, ref TempFile);
					num2++;
					Gen_Table(104, 15269, 0, ref TempFile);
					num2++;
					Revert_Mode_Mutate();
				}
			}
			else if ((ComboBox1.SelectedIndex == 6) | (ComboBox1.SelectedIndex == 7))
			{
				if (CheckBox4.Checked)
				{
					Gen_Table(100, 15028, 1, ref TempFile);
					num2++;
					Gen_Table(100, 15034, 2, ref TempFile);
					num2++;
					Gen_Table(101, 39487, 2, ref TempFile);
					num2++;
					Gen_Table(101, 39488, 1, ref TempFile);
					num2++;
					Gen_Table(102, 15020, 0, ref TempFile);
					num2++;
					Gen_Table(103, 15200, 0, ref TempFile);
					num2++;
					Gen_Table(104, 15205, 0, ref TempFile);
					num2++;
					if (CheckBox10.Checked)
					{
						Gen_Table(105, 15247, 0, ref TempFile);
						num2++;
						Gen_Table(105, 15246, 0, ref TempFile);
						num2++;
						Gen_Table(101, 39433, 0, ref TempFile);
						num2++;
						Gen_Table(101, 39434, 0, ref TempFile);
						num2++;
						Gen_Table(103, 39420, 1, ref TempFile);
						num2++;
						Gen_Table(103, 39419, 2, ref TempFile);
						num2++;
					}
				}
				if (CheckBox5.Checked)
				{
					Apply_Mode_Mutate(ComboBox3.SelectedIndex);
					Gen_Table(100, 15030, 1, ref TempFile);
					num2++;
					Gen_Table(100, 15036, 2, ref TempFile);
					num2++;
					Gen_Table(101, 15323, 0, ref TempFile);
					num2++;
					Gen_Table(102, 15090, 0, ref TempFile);
					num2++;
					Gen_Table(103, 15285, 0, ref TempFile);
					num2++;
					Gen_Table(104, 15293, 0, ref TempFile);
					num2++;
					if (CheckBox10.Checked)
					{
						Gen_Table(105, 15288, 0, ref TempFile);
						num2++;
					}
					Revert_Mode_Mutate();
				}
				if (CheckBox6.Checked)
				{
					Apply_Mode_Mutate(ComboBox4.SelectedIndex);
					Gen_Table(100, 15031, 1, ref TempFile);
					num2++;
					Gen_Table(100, 15037, 2, ref TempFile);
					num2++;
					Gen_Table(101, 15326, 0, ref TempFile);
					num2++;
					Gen_Table(102, 15093, 0, ref TempFile);
					num2++;
					Gen_Table(103, 15289, 0, ref TempFile);
					num2++;
					Gen_Table(104, 15296, 0, ref TempFile);
					num2++;
					if (CheckBox10.Checked)
					{
						Gen_Table(105, 15292, 0, ref TempFile);
						num2++;
					}
					Revert_Mode_Mutate();
				}
				if (CheckBox18.Checked)
				{
					Gen_Table(100, 539, 1, ref TempFile);
					num2++;
					Gen_Table(100, 537, 2, ref TempFile);
					num2++;
					Gen_Table(101, 538, 0, ref TempFile);
					num2++;
					Gen_Table(102, 536, 0, ref TempFile);
					num2++;
					Gen_Table(103, 11652, 0, ref TempFile);
					num2++;
					Gen_Table(104, 11646, 0, ref TempFile);
					num2++;
					if (CheckBox10.Checked)
					{
						Gen_Table(105, 540, 0, ref TempFile);
						num2++;
					}
				}
				if (CheckBox7.Checked)
				{
					Gen_Table(100, 15029, 1, ref TempFile);
					num2++;
					Gen_Table(100, 15035, 2, ref TempFile);
					num2++;
					Gen_Table(101, 15012, 0, ref TempFile);
					num2++;
					Gen_Table(101, 15017, 0, ref TempFile);
					num2++;
					Gen_Table(102, 15022, 0, ref TempFile);
					num2++;
					Gen_Table(102, 15027, 0, ref TempFile);
					num2++;
					Gen_Table(103, 15202, 0, ref TempFile);
					num2++;
					Gen_Table(104, 15206, 0, ref TempFile);
					num2++;
					Gen_Table(104, 15267, 0, ref TempFile);
					num2++;
					if (CheckBox10.Checked)
					{
						Gen_Table(105, 15249, 0, ref TempFile);
						num2++;
					}
				}
				if (CheckBox3.Checked)
				{
					Gen_Table(138, 15033, 1, ref TempFile);
					num2++;
					Gen_Table(138, 15039, 2, ref TempFile);
					num2++;
					Gen_Table(138, 15032, 1, ref TempFile);
					num2++;
					Gen_Table(138, 15038, 2, ref TempFile);
					num2++;
					Gen_Table(141, 15015, 0, ref TempFile);
					num2++;
					Gen_Table(139, 15025, 0, ref TempFile);
					num2++;
					Gen_Table(140, 15241, 1, ref TempFile);
					num2++;
					Gen_Table(140, 15240, 2, ref TempFile);
					num2++;
					Gen_Table(140, 15245, 1, ref TempFile);
					num2++;
					Gen_Table(140, 15244, 2, ref TempFile);
					num2++;
				}
				if (CheckBox13.Checked)
				{
					Apply_Mode_Mutate(10);
					Gen_Table(100, 39424, 1, ref TempFile);
					num2++;
					Gen_Table(100, 39425, 2, ref TempFile);
					num2++;
					Gen_Table(101, 15014, 0, ref TempFile);
					num2++;
					Gen_Table(102, 15024, 0, ref TempFile);
					num2++;
					Gen_Table(103, 15204, 0, ref TempFile);
					num2++;
					Gen_Table(104, 15269, 0, ref TempFile);
					num2++;
					Revert_Mode_Mutate();
				}
			}
			w_byte(ref TempFile, 0);
			w_byte(ref TempFile, 0);
			w_byte(ref TempFile, 0);
			w_byte(ref TempFile, 0);
			TempFile.Position = num3;
			w_lsb_int(ref TempFile, (ushort)num2);
			TempFile.Close();
			MyProject.Forms.Main_Form.Metric.Checked = num5 != 0;
			Update_VSS();
		}
	}

	private void table_disp(ref table_type tb)
	{
		Label7.Text = tb.nm;
		checked
		{
			Export_Grid.Cell_CharMax = (byte)tb.fw;
			Export_Grid.Grid_X = tb.table_x;
			Export_Grid.Grid_Y = tb.table_y;
			int table_y = tb.table_y;
			for (int i = 1; i <= table_y; i++)
			{
				int table_x = tb.table_x;
				for (int j = 1; j <= table_x; j++)
				{
					Export_Grid.W_Data((byte)j, (byte)i, tb.table[j, i]);
				}
			}
		}
	}

	private void w_string(ref FileStream TempFile, string TempS)
	{
		int num = Strings.Len(TempS);
		checked
		{
			for (int i = 1; i <= num; i++)
			{
				byte value = (byte)Strings.Asc(Strings.Mid(TempS, i, 1));
				TempFile.WriteByte(value);
			}
		}
	}

	private void w_byte(ref FileStream TempFile, byte tempb)
	{
		TempFile.WriteByte(tempb);
	}

	private void w_int(ref FileStream TempFile, ushort tempi)
	{
		checked
		{
			byte value = (byte)Math.Round(Conversion.Int((double)unchecked((int)tempi) / 256.0));
			byte value2 = (byte)unchecked(tempi % 256);
			TempFile.WriteByte(value);
			TempFile.WriteByte(value2);
		}
	}

	private void w_lsb_int(ref FileStream TempFile, ushort tempi)
	{
		checked
		{
			byte value = (byte)Math.Round(Conversion.Int((double)unchecked((int)tempi) / 256.0));
			byte value2 = (byte)unchecked(tempi % 256);
			TempFile.WriteByte(value2);
			TempFile.WriteByte(value);
		}
	}

	private void table_out(ref FileStream TempFile, ref table_type tb)
	{
		w_lsb_int(ref TempFile, tb.tn);
		checked
		{
			uint num = (uint)TempFile.Position;
			w_lsb_int(ref TempFile, 0);
			uint num2 = (uint)TempFile.Position;
			if (Operators.CompareString(tb.units, "", false) != 0)
			{
				w_string(ref TempFile, tb.units);
			}
			w_byte(ref TempFile, 9);
			int table_x = tb.table_x;
			for (int i = 1; i <= table_x; i++)
			{
				w_string(ref TempFile, tb.xaxis[i - 1]);
				w_byte(ref TempFile, 9);
			}
			if (Operators.CompareString(tb.xunits, "", false) != 0)
			{
				w_string(ref TempFile, tb.xunits);
			}
			w_byte(ref TempFile, 13);
			w_byte(ref TempFile, 10);
			int table_y = tb.table_y;
			for (int j = 1; j <= table_y; j++)
			{
				w_string(ref TempFile, tb.yaxis[j - 1]);
				w_byte(ref TempFile, 9);
				int table_x2 = tb.table_x;
				for (int k = 1; k <= table_x2; k++)
				{
					w_string(ref TempFile, Strings.Format((object)tb.table[k, j], ""));
					w_byte(ref TempFile, 9);
				}
				TempFile.Position -= 1;
				w_byte(ref TempFile, 13);
				w_byte(ref TempFile, 10);
			}
			if (Operators.CompareString(tb.yunits, "", false) != 0)
			{
				w_string(ref TempFile, tb.yunits);
			}
			uint num3 = (uint)TempFile.Position;
			ushort num4 = (ushort)(num3 - num2);
			byte b = (byte)unchecked(num4 / 128);
			byte tempb = (byte)(num4 - (b - 1) * 128);
			TempFile.Position = num;
			w_byte(ref TempFile, tempb);
			w_byte(ref TempFile, b);
			TempFile.Position = num3;
		}
	}

	private void c_out(ref FileStream TempFile, short tn, double c, byte u)
	{
		byte[] bytes = BitConverter.GetBytes(c);
		checked
		{
			w_lsb_int(ref TempFile, (ushort)tn);
			int num = 0;
			do
			{
				w_byte(ref TempFile, bytes[num]);
				num++;
			}
			while (num <= 7);
			w_byte(ref TempFile, u);
		}
	}

	private void Apply_Mode_Mutate(int opt)
	{
		if (opt < 1)
		{
			return;
		}
		ms_DM = MyProject.Forms.Main_Form.DynoMode.Checked;
		ms_RRM = MyProject.Forms.Main_Form.RRM.Checked;
		ms_SGS = MyProject.Forms.Main_Form.SGS.Checked;
		ms_Gear = MyProject.Forms.Main_Form.Gear.Value;
		ms_DRPM = MyProject.Forms.Main_Form.DRPM.Value;
		ms_Factor = MyProject.Forms.Main_Form.Factor.Value;
		ms_Offset = MyProject.Forms.Main_Form.Offset.Value;
		ms_UpF = MyProject.Forms.Main_Form.UpF.Value;
		ms_DownF = MyProject.Forms.Main_Form.DownF.Value;
		ms_WotLck = MyProject.Forms.Main_Form.WotLck.Value;
		ms_SlopeCombo = MyProject.Forms.Main_Form.ComboBox2.SelectedIndex;
		checked
		{
			ms_RPM = new float[MyProject.Forms.Main_Form.RPM.Grid_Y + 1];
			int grid_Y = MyProject.Forms.Main_Form.RPM.Grid_Y;
			for (int i = 1; i <= grid_Y; i++)
			{
				ms_RPM[i] = MyProject.Forms.Main_Form.RPM.R_Data(1, (byte)i);
			}
			ms_MinTCC = new float[MyProject.Forms.TCC_Form.MinTCC.Grid_X + 1, MyProject.Forms.TCC_Form.MinTCC.Grid_Y + 1];
			int grid_Y2 = MyProject.Forms.TCC_Form.MinTCC.Grid_Y;
			for (int j = 1; j <= grid_Y2; j++)
			{
				int grid_X = MyProject.Forms.TCC_Form.MinTCC.Grid_X;
				for (int k = 1; k <= grid_X; k++)
				{
					ms_MinTCC[k, j] = MyProject.Forms.TCC_Form.MinTCC.R_Data((byte)k, (byte)j);
				}
			}
			ms_active = true;
			switch (opt)
			{
			case 1:
			{
				float num = 0f;
				int grid_Y3 = MyProject.Forms.Main_Form.RPM.Grid_Y;
				for (int l = 1; l <= grid_Y3; l++)
				{
					if (ms_RPM[l] > num)
					{
						num = ms_RPM[l];
					}
				}
				float num2 = 0f;
				int grid_Y4 = MyProject.Forms.Main_Form.RPM.Grid_Y;
				for (int m = 1; m <= grid_Y4; m++)
				{
					float num3 = ms_RPM[m] - 1000f;
					if (num3 < 5250f)
					{
						num3 = 5250f;
					}
					MyProject.Forms.Main_Form.RPM.W_Data(1, (byte)m, num3);
					if (num3 > num2)
					{
						num2 = num3;
					}
				}
				float num4 = num2 - 750f;
				if (num4 < Convert.ToSingle(MyProject.Forms.Main_Form.DRPM.Minimum))
				{
					num4 = Convert.ToSingle(MyProject.Forms.Main_Form.DRPM.Minimum);
				}
				if (num4 > Convert.ToSingle(MyProject.Forms.Main_Form.DRPM.Maximum))
				{
					num4 = Convert.ToSingle(MyProject.Forms.Main_Form.DRPM.Maximum);
				}
				MyProject.Forms.Main_Form.DRPM.Value = new decimal(num4);
				decimal num5 = decimal.Subtract(ms_Offset, 3m);
				if (decimal.Compare(num5, MyProject.Forms.Main_Form.Offset.Minimum) < 0)
				{
					num5 = MyProject.Forms.Main_Form.Offset.Minimum;
				}
				MyProject.Forms.Main_Form.Offset.Value = num5;
				decimal num6 = decimal.Add(ms_UpF, 1m);
				if (decimal.Compare(num6, MyProject.Forms.Main_Form.UpF.Maximum) > 0)
				{
					num6 = MyProject.Forms.Main_Form.UpF.Maximum;
				}
				MyProject.Forms.Main_Form.UpF.Value = num6;
				decimal num7 = decimal.Add(ms_DownF, 1m);
				if (decimal.Compare(num7, MyProject.Forms.Main_Form.DownF.Maximum) > 0)
				{
					num7 = MyProject.Forms.Main_Form.DownF.Maximum;
				}
				MyProject.Forms.Main_Form.DownF.Value = num7;
				MyProject.Forms.Main_Form.WotLck.Value = MyProject.Forms.Main_Form.MinLck.Value;
				float d = (float)((double)num * 0.33);
				int grid_Y5 = MyProject.Forms.TCC_Form.MinTCC.Grid_Y;
				for (int n = 1; n <= grid_Y5; n += 2)
				{
					int grid_X2 = MyProject.Forms.TCC_Form.MinTCC.Grid_X;
					for (int num8 = 1; num8 <= grid_X2; num8++)
					{
						MyProject.Forms.TCC_Form.MinTCC.W_Data((byte)num8, (byte)n, d);
					}
				}
				break;
			}
			case 2:
				MyProject.Forms.Main_Form.DynoMode.Checked = true;
				break;
			case 3:
				MyProject.Forms.Main_Form.RRM.Checked = true;
				break;
			case 4:
				MyProject.Forms.Main_Form.SGS.Checked = true;
				break;
			case 10:
				MyProject.Forms.Main_Form.Gear.Value = decimal.Multiply(ms_Gear, Gear.Value);
				break;
			}
			MyProject.Forms.Main_Form.Update_Slope();
			MyProject.Forms.Main_Form.Calc_Shifts();
		}
	}

	private void Revert_Mode_Mutate()
	{
		if (!ms_active)
		{
			return;
		}
		MyProject.Forms.Main_Form.DynoMode.Checked = ms_DM;
		MyProject.Forms.Main_Form.RRM.Checked = ms_RRM;
		MyProject.Forms.Main_Form.SGS.Checked = ms_SGS;
		MyProject.Forms.Main_Form.Gear.Value = ms_Gear;
		MyProject.Forms.Main_Form.DRPM.Value = ms_DRPM;
		MyProject.Forms.Main_Form.WotLck.Value = ms_WotLck;
		int grid_Y = MyProject.Forms.Main_Form.RPM.Grid_Y;
		checked
		{
			for (int i = 1; i <= grid_Y; i++)
			{
				MyProject.Forms.Main_Form.RPM.W_Data(1, (byte)i, ms_RPM[i]);
			}
			int grid_Y2 = MyProject.Forms.TCC_Form.MinTCC.Grid_Y;
			for (int j = 1; j <= grid_Y2; j++)
			{
				int grid_X = MyProject.Forms.TCC_Form.MinTCC.Grid_X;
				for (int k = 1; k <= grid_X; k++)
				{
					MyProject.Forms.TCC_Form.MinTCC.W_Data((byte)k, (byte)j, ms_MinTCC[k, j]);
				}
			}
			MyProject.Forms.Main_Form.Factor.Value = ms_Factor;
			MyProject.Forms.Main_Form.Offset.Value = ms_Offset;
			MyProject.Forms.Main_Form.UpF.Value = ms_UpF;
			MyProject.Forms.Main_Form.DownF.Value = ms_DownF;
			MyProject.Forms.Main_Form.ComboBox2.SelectedIndex = ms_SlopeCombo;
			ms_active = false;
			MyProject.Forms.Main_Form.Update_Slope();
			MyProject.Forms.Main_Form.Calc_Shifts();
		}
	}

	private void Export_Form_Load(object sender, EventArgs e)
	{
		ComboBox3.SelectedIndex = 0;
		ComboBox4.SelectedIndex = 0;
		ComboBox1.DrawMode = (DrawMode)1;
		ComboBox2.DrawMode = (DrawMode)1;
	}

	private void CheckBox17_CheckedChanged(object sender, EventArgs e)
	{
		if (CheckBox17.Checked)
		{
			((Control)NDTire).Enabled = true;
			return;
		}
		((Control)NDTire).Enabled = false;
		NDTire.Value = MyProject.Forms.Main_Form.TireVisible.Value;
	}

	private void NDTire_ValueChanged(object sender, EventArgs e)
	{
		if (Init != 0)
		{
			MyProject.Forms.Main_Form.US = checked((ushort)(MyProject.Forms.Main_Form.US + 1));
		}
	}

	private void Export_Form_Shown(object sender, EventArgs e)
	{
		Init = 1;
	}

	private void CheckBox21_CheckedChanged(object sender, EventArgs e)
	{
		if (CheckBox21.Checked)
		{
			((Form)this).TopMost = true;
		}
		else
		{
			((Form)this).TopMost = false;
		}
	}
}
