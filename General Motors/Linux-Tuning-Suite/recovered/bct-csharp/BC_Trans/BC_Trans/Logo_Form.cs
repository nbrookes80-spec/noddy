using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.Runtime.CompilerServices;
using System.Windows.Forms;
using Microsoft.VisualBasic.CompilerServices;

namespace BC_Trans;

[DesignerGenerated]
public class Logo_Form : Form
{
	private IContainer components;

	[AccessedThroughProperty("Timer1")]
	private Timer _Timer1;

	private int C;

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

	[DebuggerNonUserCode]
	public Logo_Form()
	{
		//IL_000f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0019: Expected O, but got Unknown
		((Control)this).MouseClick += new MouseEventHandler(Logo_Form_MouseClick);
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
		//IL_0069: Unknown result type (might be due to invalid IL or missing references)
		//IL_0073: Expected O, but got Unknown
		components = new Container();
		ComponentResourceManager componentResourceManager = new ComponentResourceManager(typeof(Logo_Form));
		Timer1 = new Timer(components);
		((Control)this).SuspendLayout();
		Timer1.Enabled = true;
		SizeF autoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleDimensions = autoScaleDimensions;
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Control)this).BackgroundImage = (Image)componentResourceManager.GetObject("$this.BackgroundImage");
		((Control)this).BackgroundImageLayout = (ImageLayout)3;
		Size clientSize = new Size(527, 151);
		((Form)this).ClientSize = clientSize;
		((Form)this).ControlBox = false;
		((Control)this).DoubleBuffered = true;
		((Form)this).FormBorderStyle = (FormBorderStyle)3;
		((Form)this).MaximizeBox = false;
		((Form)this).MinimizeBox = false;
		((Control)this).Name = "Logo_Form";
		((Form)this).ShowIcon = false;
		((Form)this).ShowInTaskbar = false;
		((Form)this).StartPosition = (FormStartPosition)1;
		((Form)this).TransparencyKey = Color.Green;
		((Control)this).ResumeLayout(false);
	}

	private void Timer1_Tick(object sender, EventArgs e)
	{
		checked
		{
			C++;
			if (C == 2)
			{
				((Control)this).Show();
				((Control)this).BringToFront();
				((Form)this).Opacity = 0.999;
			}
			if (C > 20)
			{
				((Form)this).Opacity = ((Form)this).Opacity - 0.05;
			}
			if (((Form)this).Opacity <= 0.0)
			{
				((Control)this).Hide();
				((Control)this).Enabled = false;
				Timer1.Enabled = false;
				((Component)(object)this).Dispose();
			}
		}
	}

	private void Logo_Form_MouseClick(object sender, MouseEventArgs e)
	{
		((Control)this).Hide();
		((Control)this).Enabled = false;
		Timer1.Enabled = false;
		((Component)(object)this).Dispose();
	}
}
