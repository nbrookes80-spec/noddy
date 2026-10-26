using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.Runtime.CompilerServices;
using System.Windows.Forms;
using BC_Trans.My;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.CompilerServices;

namespace BC_Trans;

[DesignerGenerated]
public class Tire_Form : Form
{
	private IContainer components;

	[AccessedThroughProperty("Label1")]
	private Label _Label1;

	[AccessedThroughProperty("TextBox2")]
	private TextBox _TextBox2;

	[AccessedThroughProperty("TextBox1")]
	private TextBox _TextBox1;

	[AccessedThroughProperty("Label2")]
	private Label _Label2;

	[AccessedThroughProperty("TextBox3")]
	private TextBox _TextBox3;

	[AccessedThroughProperty("RadioButton1")]
	private RadioButton _RadioButton1;

	[AccessedThroughProperty("RadioButton2")]
	private RadioButton _RadioButton2;

	[AccessedThroughProperty("GroupBox1")]
	private GroupBox _GroupBox1;

	[AccessedThroughProperty("Button1")]
	private Button _Button1;

	[AccessedThroughProperty("GroupBox2")]
	private GroupBox _GroupBox2;

	[AccessedThroughProperty("Label3")]
	private Label _Label3;

	[AccessedThroughProperty("TextBox4")]
	private TextBox _TextBox4;

	[AccessedThroughProperty("Label7")]
	private Label _Label7;

	[AccessedThroughProperty("Label8")]
	private Label _Label8;

	[AccessedThroughProperty("TextBox6")]
	private TextBox _TextBox6;

	[AccessedThroughProperty("Label5")]
	private Label _Label5;

	[AccessedThroughProperty("Label6")]
	private Label _Label6;

	[AccessedThroughProperty("TextBox5")]
	private TextBox _TextBox5;

	[AccessedThroughProperty("Label4")]
	private Label _Label4;

	[AccessedThroughProperty("Label9")]
	private Label _Label9;

	[AccessedThroughProperty("TextBox7")]
	private TextBox _TextBox7;

	[AccessedThroughProperty("Button2")]
	private Button _Button2;

	[AccessedThroughProperty("Label10")]
	private Label _Label10;

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

	internal virtual RadioButton RadioButton1
	{
		[DebuggerNonUserCode]
		get
		{
			return _RadioButton1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = RadioButton1_CheckedChanged;
			if (_RadioButton1 != null)
			{
				_RadioButton1.CheckedChanged -= eventHandler;
			}
			_RadioButton1 = value;
			if (_RadioButton1 != null)
			{
				_RadioButton1.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual RadioButton RadioButton2
	{
		[DebuggerNonUserCode]
		get
		{
			return _RadioButton2;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = RadioButton2_CheckedChanged;
			if (_RadioButton2 != null)
			{
				_RadioButton2.CheckedChanged -= eventHandler;
			}
			_RadioButton2 = value;
			if (_RadioButton2 != null)
			{
				_RadioButton2.CheckedChanged += eventHandler;
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

	internal virtual TextBox TextBox6
	{
		[DebuggerNonUserCode]
		get
		{
			return _TextBox6;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_TextBox6 = value;
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

	internal virtual TextBox TextBox7
	{
		[DebuggerNonUserCode]
		get
		{
			return _TextBox7;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_TextBox7 = value;
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

	[DebuggerNonUserCode]
	public Tire_Form()
	{
		((Form)this).Shown += TCC_Form_Shown;
		((Form)this).Closing += Form_Closing;
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
		//IL_0011: Unknown result type (might be due to invalid IL or missing references)
		//IL_001b: Expected O, but got Unknown
		//IL_001c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0026: Expected O, but got Unknown
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
		//IL_00b6: Unknown result type (might be due to invalid IL or missing references)
		//IL_00c0: Expected O, but got Unknown
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
		//IL_0d78: Unknown result type (might be due to invalid IL or missing references)
		//IL_0d82: Expected O, but got Unknown
		ComponentResourceManager componentResourceManager = new ComponentResourceManager(typeof(Tire_Form));
		Label1 = new Label();
		TextBox2 = new TextBox();
		TextBox1 = new TextBox();
		Label2 = new Label();
		TextBox3 = new TextBox();
		RadioButton1 = new RadioButton();
		RadioButton2 = new RadioButton();
		GroupBox1 = new GroupBox();
		Button1 = new Button();
		GroupBox2 = new GroupBox();
		Label7 = new Label();
		Label8 = new Label();
		TextBox6 = new TextBox();
		Label5 = new Label();
		Label6 = new Label();
		TextBox5 = new TextBox();
		Label4 = new Label();
		Label3 = new Label();
		TextBox4 = new TextBox();
		Label9 = new Label();
		TextBox7 = new TextBox();
		Button2 = new Button();
		Label10 = new Label();
		((Control)GroupBox1).SuspendLayout();
		((Control)GroupBox2).SuspendLayout();
		((Control)this).SuspendLayout();
		Label1.AutoSize = true;
		Label label = Label1;
		Point location = new Point(66, 22);
		((Control)label).Location = location;
		((Control)Label1).Name = "Label1";
		Label label2 = Label1;
		Size size = new Size(12, 13);
		((Control)label2).Size = size;
		((Control)Label1).TabIndex = 5;
		Label1.Text = "/";
		((TextBoxBase)TextBox2).BackColor = SystemColors.Window;
		TextBox textBox = TextBox2;
		location = new Point(84, 19);
		((Control)textBox).Location = location;
		((Control)TextBox2).Name = "TextBox2";
		TextBox textBox2 = TextBox2;
		size = new Size(57, 20);
		((Control)textBox2).Size = size;
		((Control)TextBox2).TabIndex = 6;
		TextBox2.Text = "60";
		TextBox2.TextAlign = (HorizontalAlignment)2;
		((TextBoxBase)TextBox1).BackColor = SystemColors.Window;
		TextBox textBox3 = TextBox1;
		location = new Point(6, 19);
		((Control)textBox3).Location = location;
		((Control)TextBox1).Name = "TextBox1";
		TextBox textBox4 = TextBox1;
		size = new Size(57, 20);
		((Control)textBox4).Size = size;
		((Control)TextBox1).TabIndex = 4;
		TextBox1.Text = "275";
		TextBox1.TextAlign = (HorizontalAlignment)2;
		Label2.AutoSize = true;
		Label label3 = Label2;
		location = new Point(147, 22);
		((Control)label3).Location = location;
		((Control)Label2).Name = "Label2";
		Label label4 = Label2;
		size = new Size(15, 13);
		((Control)label4).Size = size;
		((Control)Label2).TabIndex = 7;
		Label2.Text = "R";
		((TextBoxBase)TextBox3).BackColor = SystemColors.Window;
		TextBox textBox5 = TextBox3;
		location = new Point(168, 19);
		((Control)textBox5).Location = location;
		((Control)TextBox3).Name = "TextBox3";
		TextBox textBox6 = TextBox3;
		size = new Size(57, 20);
		((Control)textBox6).Size = size;
		((Control)TextBox3).TabIndex = 8;
		TextBox3.Text = "15";
		TextBox3.TextAlign = (HorizontalAlignment)2;
		((ButtonBase)RadioButton1).AutoSize = true;
		RadioButton1.Checked = true;
		RadioButton radioButton = RadioButton1;
		location = new Point(6, 45);
		((Control)radioButton).Location = location;
		((Control)RadioButton1).Name = "RadioButton1";
		RadioButton radioButton2 = RadioButton1;
		size = new Size(54, 17);
		((Control)radioButton2).Size = size;
		((Control)RadioButton1).TabIndex = 9;
		RadioButton1.TabStop = true;
		((ButtonBase)RadioButton1).Text = "Metric";
		((ButtonBase)RadioButton1).UseVisualStyleBackColor = true;
		((ButtonBase)RadioButton2).AutoSize = true;
		RadioButton radioButton3 = RadioButton2;
		location = new Point(6, 68);
		((Control)radioButton3).Location = location;
		((Control)RadioButton2).Name = "RadioButton2";
		RadioButton radioButton4 = RadioButton2;
		size = new Size(61, 17);
		((Control)radioButton4).Size = size;
		((Control)RadioButton2).TabIndex = 10;
		((ButtonBase)RadioButton2).Text = "Imperial";
		((ButtonBase)RadioButton2).UseVisualStyleBackColor = true;
		((Control)GroupBox1).Controls.Add((Control)(object)Button1);
		((Control)GroupBox1).Controls.Add((Control)(object)TextBox1);
		((Control)GroupBox1).Controls.Add((Control)(object)RadioButton2);
		((Control)GroupBox1).Controls.Add((Control)(object)TextBox2);
		((Control)GroupBox1).Controls.Add((Control)(object)RadioButton1);
		((Control)GroupBox1).Controls.Add((Control)(object)Label1);
		((Control)GroupBox1).Controls.Add((Control)(object)TextBox3);
		((Control)GroupBox1).Controls.Add((Control)(object)Label2);
		GroupBox groupBox = GroupBox1;
		location = new Point(12, 12);
		((Control)groupBox).Location = location;
		((Control)GroupBox1).Name = "GroupBox1";
		GroupBox groupBox2 = GroupBox1;
		size = new Size(234, 96);
		((Control)groupBox2).Size = size;
		((Control)GroupBox1).TabIndex = 11;
		GroupBox1.TabStop = false;
		GroupBox1.Text = "Input";
		Button button = Button1;
		location = new Point(76, 51);
		((Control)button).Location = location;
		((Control)Button1).Name = "Button1";
		Button button2 = Button1;
		size = new Size(148, 33);
		((Control)button2).Size = size;
		((Control)Button1).TabIndex = 11;
		((ButtonBase)Button1).Text = "Calculate";
		((ButtonBase)Button1).UseVisualStyleBackColor = true;
		((Control)GroupBox2).Controls.Add((Control)(object)Label7);
		((Control)GroupBox2).Controls.Add((Control)(object)Label8);
		((Control)GroupBox2).Controls.Add((Control)(object)TextBox6);
		((Control)GroupBox2).Controls.Add((Control)(object)Label5);
		((Control)GroupBox2).Controls.Add((Control)(object)Label6);
		((Control)GroupBox2).Controls.Add((Control)(object)TextBox5);
		((Control)GroupBox2).Controls.Add((Control)(object)Label4);
		((Control)GroupBox2).Controls.Add((Control)(object)Label3);
		((Control)GroupBox2).Controls.Add((Control)(object)TextBox4);
		GroupBox groupBox3 = GroupBox2;
		location = new Point(13, 118);
		((Control)groupBox3).Location = location;
		((Control)GroupBox2).Name = "GroupBox2";
		GroupBox groupBox4 = GroupBox2;
		size = new Size(232, 116);
		((Control)groupBox4).Size = size;
		((Control)GroupBox2).TabIndex = 12;
		GroupBox2.TabStop = false;
		GroupBox2.Text = "Output";
		Label7.AutoSize = true;
		Label label5 = Label7;
		location = new Point(185, 85);
		((Control)label5).Location = location;
		((Control)Label7).Name = "Label7";
		Label label6 = Label7;
		size = new Size(15, 13);
		((Control)label6).Size = size;
		((Control)Label7).TabIndex = 15;
		Label7.Text = "in";
		Label8.AutoSize = true;
		Label label7 = Label8;
		location = new Point(6, 85);
		((Control)label7).Location = location;
		((Control)Label8).Name = "Label8";
		Label label8 = Label8;
		size = new Size(92, 13);
		((Control)label8).Size = size;
		((Control)Label8).TabIndex = 14;
		Label8.Text = "Est. Actual Height";
		((TextBoxBase)TextBox6).BackColor = SystemColors.Window;
		TextBox textBox7 = TextBox6;
		location = new Point(106, 82);
		((Control)textBox7).Location = location;
		((Control)TextBox6).Name = "TextBox6";
		((TextBoxBase)TextBox6).ReadOnly = true;
		TextBox textBox8 = TextBox6;
		size = new Size(69, 20);
		((Control)textBox8).Size = size;
		((Control)TextBox6).TabIndex = 13;
		TextBox6.Text = "27.6";
		TextBox6.TextAlign = (HorizontalAlignment)1;
		Label5.AutoSize = true;
		Label label9 = Label5;
		location = new Point(185, 48);
		((Control)label9).Location = location;
		((Control)Label5).Name = "Label5";
		Label label10 = Label5;
		size = new Size(15, 13);
		((Control)label10).Size = size;
		((Control)Label5).TabIndex = 12;
		Label5.Text = "in";
		Label6.AutoSize = true;
		Label label11 = Label6;
		location = new Point(6, 48);
		((Control)label11).Location = location;
		((Control)Label6).Name = "Label6";
		Label label12 = Label6;
		size = new Size(38, 13);
		((Control)label12).Size = size;
		((Control)Label6).TabIndex = 11;
		Label6.Text = "Height";
		((TextBoxBase)TextBox5).BackColor = SystemColors.Window;
		TextBox textBox9 = TextBox5;
		location = new Point(106, 45);
		((Control)textBox9).Location = location;
		((Control)TextBox5).Name = "TextBox5";
		((TextBoxBase)TextBox5).ReadOnly = true;
		TextBox textBox10 = TextBox5;
		size = new Size(69, 20);
		((Control)textBox10).Size = size;
		((Control)TextBox5).TabIndex = 10;
		TextBox5.Text = "28";
		TextBox5.TextAlign = (HorizontalAlignment)1;
		Label4.AutoSize = true;
		Label label13 = Label4;
		location = new Point(185, 22);
		((Control)label13).Location = location;
		((Control)Label4).Name = "Label4";
		Label label14 = Label4;
		size = new Size(15, 13);
		((Control)label14).Size = size;
		((Control)Label4).TabIndex = 9;
		Label4.Text = "in";
		Label3.AutoSize = true;
		Label label15 = Label3;
		location = new Point(6, 22);
		((Control)label15).Location = location;
		((Control)Label3).Name = "Label3";
		Label label16 = Label3;
		size = new Size(35, 13);
		((Control)label16).Size = size;
		((Control)Label3).TabIndex = 8;
		Label3.Text = "Width";
		((TextBoxBase)TextBox4).BackColor = SystemColors.Window;
		TextBox textBox11 = TextBox4;
		location = new Point(106, 19);
		((Control)textBox11).Location = location;
		((Control)TextBox4).Name = "TextBox4";
		((TextBoxBase)TextBox4).ReadOnly = true;
		TextBox textBox12 = TextBox4;
		size = new Size(69, 20);
		((Control)textBox12).Size = size;
		((Control)TextBox4).TabIndex = 7;
		TextBox4.Text = "8.5";
		TextBox4.TextAlign = (HorizontalAlignment)1;
		Label9.AutoSize = true;
		Label label17 = Label9;
		location = new Point(19, 243);
		((Control)label17).Location = location;
		((Control)Label9).Name = "Label9";
		Label label18 = Label9;
		size = new Size(79, 13);
		((Control)label18).Size = size;
		((Control)Label9).TabIndex = 17;
		Label9.Text = "Height to Apply";
		((TextBoxBase)TextBox7).BackColor = SystemColors.Window;
		TextBox textBox13 = TextBox7;
		location = new Point(119, 240);
		((Control)textBox13).Location = location;
		((Control)TextBox7).Name = "TextBox7";
		TextBox textBox14 = TextBox7;
		size = new Size(69, 20);
		((Control)textBox14).Size = size;
		((Control)TextBox7).TabIndex = 16;
		TextBox7.Text = "27.6";
		TextBox7.TextAlign = (HorizontalAlignment)1;
		Button button3 = Button2;
		location = new Point(12, 273);
		((Control)button3).Location = location;
		((Control)Button2).Name = "Button2";
		Button button4 = Button2;
		size = new Size(233, 33);
		((Control)button4).Size = size;
		((Control)Button2).TabIndex = 18;
		((ButtonBase)Button2).Text = "Apply";
		((ButtonBase)Button2).UseVisualStyleBackColor = true;
		Label10.AutoSize = true;
		Label label19 = Label10;
		location = new Point(198, 243);
		((Control)label19).Location = location;
		((Control)Label10).Name = "Label10";
		Label label20 = Label10;
		size = new Size(15, 13);
		((Control)label20).Size = size;
		((Control)Label10).TabIndex = 19;
		Label10.Text = "in";
		SizeF autoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleDimensions = autoScaleDimensions;
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		size = new Size(258, 318);
		((Form)this).ClientSize = size;
		((Control)this).Controls.Add((Control)(object)Label10);
		((Control)this).Controls.Add((Control)(object)Button2);
		((Control)this).Controls.Add((Control)(object)Label9);
		((Control)this).Controls.Add((Control)(object)TextBox7);
		((Control)this).Controls.Add((Control)(object)GroupBox2);
		((Control)this).Controls.Add((Control)(object)GroupBox1);
		((Control)this).DoubleBuffered = true;
		((Form)this).FormBorderStyle = (FormBorderStyle)1;
		((Form)this).Icon = (Icon)componentResourceManager.GetObject("$this.Icon");
		((Form)this).MaximizeBox = false;
		((Control)this).Name = "Tire_Form";
		((Form)this).StartPosition = (FormStartPosition)1;
		((Form)this).Text = "Tire Size Conversion";
		((Control)GroupBox1).ResumeLayout(false);
		((Control)GroupBox1).PerformLayout();
		((Control)GroupBox2).ResumeLayout(false);
		((Control)GroupBox2).PerformLayout();
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
		Button1_Click(null, null);
	}

	private void RadioButton1_CheckedChanged(object sender, EventArgs e)
	{
		if (RadioButton1.Checked)
		{
			Label1.Text = "/";
		}
	}

	private void RadioButton2_CheckedChanged(object sender, EventArgs e)
	{
		if (RadioButton2.Checked)
		{
			Label1.Text = "x";
		}
	}

	public void Button1_Click(object sender, EventArgs e)
	{
		double num = Conversion.Val(TextBox1.Text);
		double num2 = Conversion.Val(TextBox2.Text);
		double num3 = Conversion.Val(TextBox3.Text);
		if (!MyProject.Forms.Main_Form.Metric.Checked)
		{
			if (RadioButton1.Checked)
			{
				TextBox4.Text = Strings.Format((object)(2.0 * num * (1.0 - num2 / 100.0) / 25.4), "####.###");
				TextBox5.Text = Strings.Format((object)(2.0 * num * (num2 / 100.0) / 25.4 + num3), "####.###");
				TextBox6.Text = Strings.Format((object)(Conversion.Val(TextBox5.Text) * 0.985), "####.###");
			}
			else if (RadioButton2.Checked)
			{
				TextBox4.Text = Strings.Format((object)num2, "####.###");
				TextBox5.Text = Strings.Format((object)num, "####.###");
				TextBox6.Text = Strings.Format((object)(Conversion.Val(TextBox5.Text) * 0.965), "####.###");
			}
			TextBox7.Text = Strings.Format((object)Conversion.Val(TextBox6.Text), "####.##");
		}
		else
		{
			if (RadioButton1.Checked)
			{
				TextBox4.Text = Strings.Format((object)(2.0 * num * (1.0 - num2 / 100.0)), "#####.#");
				TextBox5.Text = Strings.Format((object)(2.0 * num * (num2 / 100.0) + num3 * 25.4), "#####.#");
				TextBox6.Text = Strings.Format((object)(Conversion.Val(TextBox5.Text) * 0.985), "#####.#");
			}
			else if (RadioButton2.Checked)
			{
				TextBox4.Text = Strings.Format((object)(num2 * 25.4), "#####.#");
				TextBox5.Text = Strings.Format((object)(num * 25.4), "#####.#");
				TextBox6.Text = Strings.Format((object)(Conversion.Val(TextBox5.Text) * 0.965), "#####.#");
			}
			TextBox7.Text = Strings.Format((object)Conversion.Val(TextBox6.Text), "#####");
		}
	}

	private void Button2_Click(object sender, EventArgs e)
	{
		double num = Conversion.Val(TextBox7.Text);
		if (num < Convert.ToDouble(MyProject.Forms.Main_Form.TireVisible.Minimum))
		{
			num = Convert.ToDouble(MyProject.Forms.Main_Form.TireVisible.Minimum);
		}
		if (num > Convert.ToDouble(MyProject.Forms.Main_Form.TireVisible.Maximum))
		{
			num = Convert.ToDouble(MyProject.Forms.Main_Form.TireVisible.Maximum);
		}
		MyProject.Forms.Main_Form.TireVisible.Value = new decimal(num);
		((Control)this).Hide();
		((Control)MyProject.Forms.Main_Form).Focus();
	}
}
