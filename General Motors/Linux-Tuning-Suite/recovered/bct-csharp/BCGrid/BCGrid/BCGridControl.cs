using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.Runtime.CompilerServices;
using System.Windows.Forms;
using BCGrid.My;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.CompilerServices;
using Microsoft.VisualBasic.Devices;

namespace BCGrid;

[DesignerGenerated]
public class BCGridControl : UserControl
{
	private IContainer components;

	[AccessedThroughProperty("TextBox1")]
	private TextBox _TextBox1;

	[AccessedThroughProperty("Timer1")]
	private Timer _Timer1;

	[AccessedThroughProperty("DataMenuStrip")]
	private ContextMenuStrip _DataMenuStrip;

	[AccessedThroughProperty("CopyToolStripMenuItem")]
	private ToolStripMenuItem _CopyToolStripMenuItem;

	[AccessedThroughProperty("PasteToolStripMenuItem")]
	private ToolStripMenuItem _PasteToolStripMenuItem;

	[AccessedThroughProperty("ManipulateToolStripMenuItem")]
	private ToolStripMenuItem _ManipulateToolStripMenuItem;

	[AccessedThroughProperty("GraphToolStripMenuItem")]
	private ToolStripMenuItem _GraphToolStripMenuItem;

	[AccessedThroughProperty("CopyLabelsToolStripMenuItem")]
	private ToolStripMenuItem _CopyLabelsToolStripMenuItem;

	[AccessedThroughProperty("PasteLabelsToolStripMenuItem")]
	private ToolStripMenuItem _PasteLabelsToolStripMenuItem;

	[AccessedThroughProperty("PasteLabelsInterpolateToolStripMenuItem")]
	private ToolStripMenuItem _PasteLabelsInterpolateToolStripMenuItem;

	[AccessedThroughProperty("PasteAddToolStripMenuItem")]
	private ToolStripMenuItem _PasteAddToolStripMenuItem;

	[AccessedThroughProperty("PasteSubtractToolStripMenuItem")]
	private ToolStripMenuItem _PasteSubtractToolStripMenuItem;

	[AccessedThroughProperty("PasteMultiplyToolStripMenuItem")]
	private ToolStripMenuItem _PasteMultiplyToolStripMenuItem;

	[AccessedThroughProperty("PasteMultiplyPctToolStripMenuItem")]
	private ToolStripMenuItem _PasteMultiplyPctToolStripMenuItem;

	[AccessedThroughProperty("PasteMultiplyPctHalfToolStripMenuItem")]
	private ToolStripMenuItem _PasteMultiplyPctHalfToolStripMenuItem;

	[AccessedThroughProperty("PasteDivideToolStripMenuItem")]
	private ToolStripMenuItem _PasteDivideToolStripMenuItem;

	[AccessedThroughProperty("PasteAverageToolStripMenuItem")]
	private ToolStripMenuItem _PasteAverageToolStripMenuItem;

	[AccessedThroughProperty("SmoothToolStripMenuItem")]
	private ToolStripMenuItem _SmoothToolStripMenuItem;

	[AccessedThroughProperty("SmoothHorizontalToolStripMenuItem")]
	private ToolStripMenuItem _SmoothHorizontalToolStripMenuItem;

	[AccessedThroughProperty("SmoothVerticalToolStripMenuItem")]
	private ToolStripMenuItem _SmoothVerticalToolStripMenuItem;

	[AccessedThroughProperty("InterpolateToolStripMenuItem")]
	private ToolStripMenuItem _InterpolateToolStripMenuItem;

	[AccessedThroughProperty("InterpolateHorizontalToolStripMenuItem")]
	private ToolStripMenuItem _InterpolateHorizontalToolStripMenuItem;

	[AccessedThroughProperty("InterpolateVerticalToolStripMenuItem")]
	private ToolStripMenuItem _InterpolateVerticalToolStripMenuItem;

	[AccessedThroughProperty("ExtrapolateToolStripMenuItem")]
	private ToolStripMenuItem _ExtrapolateToolStripMenuItem;

	[AccessedThroughProperty("Graph2DToolStripMenuItem")]
	private ToolStripMenuItem _Graph2DToolStripMenuItem;

	[AccessedThroughProperty("Graph3DToolStripMenuItem")]
	private ToolStripMenuItem _Graph3DToolStripMenuItem;

	[AccessedThroughProperty("ToolbarToolStripMenuItem")]
	private ToolStripMenuItem _ToolbarToolStripMenuItem;

	[AccessedThroughProperty("ToolStripSeparator2")]
	private ToolStripSeparator _ToolStripSeparator2;

	[AccessedThroughProperty("ToolStripSeparator1")]
	private ToolStripSeparator _ToolStripSeparator1;

	[AccessedThroughProperty("UndoToolStripMenuItem")]
	private ToolStripMenuItem _UndoToolStripMenuItem;

	[AccessedThroughProperty("ToolStripSeparator7")]
	private ToolStripSeparator _ToolStripSeparator7;

	[AccessedThroughProperty("ToolStripSeparator8")]
	private ToolStripSeparator _ToolStripSeparator8;

	[AccessedThroughProperty("ToolStripSeparator9")]
	private ToolStripSeparator _ToolStripSeparator9;

	[AccessedThroughProperty("ToolStripSeparator10")]
	private ToolStripSeparator _ToolStripSeparator10;

	[AccessedThroughProperty("ToolStripSeparator5")]
	private ToolStripSeparator _ToolStripSeparator5;

	[AccessedThroughProperty("ToolStripSeparator6")]
	private ToolStripSeparator _ToolStripSeparator6;

	[AccessedThroughProperty("OtherMenuItem")]
	private ToolStripMenuItem _OtherMenuItem;

	[AccessedThroughProperty("TransposeClipboardToolStripMenuItem")]
	private ToolStripMenuItem _TransposeClipboardToolStripMenuItem;

	[AccessedThroughProperty("ClearChangedFlagToolStripMenuItem")]
	private ToolStripMenuItem _ClearChangedFlagToolStripMenuItem;

	[AccessedThroughProperty("ToolStripSeparator11")]
	private ToolStripSeparator _ToolStripSeparator11;

	[AccessedThroughProperty("ToggleChangeFlagDisplayToolStripMenuItem")]
	private ToolStripMenuItem _ToggleChangeFlagDisplayToolStripMenuItem;

	[AccessedThroughProperty("ToolStripSeparator12")]
	private ToolStripSeparator _ToolStripSeparator12;

	[AccessedThroughProperty("ClearTableToZerosToolStripMenuItem")]
	private ToolStripMenuItem _ClearTableToZerosToolStripMenuItem;

	[AccessedThroughProperty("ClearTableToNullsToolStripMenuItem")]
	private ToolStripMenuItem _ClearTableToNullsToolStripMenuItem;

	[AccessedThroughProperty("ToolStripSeparator13")]
	private ToolStripSeparator _ToolStripSeparator13;

	[AccessedThroughProperty("ConvertZerosToNullsToolStripMenuItem")]
	private ToolStripMenuItem _ConvertZerosToNullsToolStripMenuItem;

	[AccessedThroughProperty("ConvertNullsToZerosToolStripMenuItem")]
	private ToolStripMenuItem _ConvertNullsToZerosToolStripMenuItem;

	[AccessedThroughProperty("ToolStripSeparator14")]
	private ToolStripSeparator _ToolStripSeparator14;

	[AccessedThroughProperty("EditToolStripMenuItem")]
	private ToolStripMenuItem _EditToolStripMenuItem;

	[AccessedThroughProperty("ToolStripTextBox1")]
	private ToolStripTextBox _ToolStripTextBox1;

	[AccessedThroughProperty("FillToolStripMenuItem")]
	private ToolStripMenuItem _FillToolStripMenuItem;

	[AccessedThroughProperty("ToolStripSeparator3")]
	private ToolStripSeparator _ToolStripSeparator3;

	[AccessedThroughProperty("AddToolStripMenuItem")]
	private ToolStripMenuItem _AddToolStripMenuItem;

	[AccessedThroughProperty("SubtractToolStripMenuItem")]
	private ToolStripMenuItem _SubtractToolStripMenuItem;

	[AccessedThroughProperty("ToolStripSeparator4")]
	private ToolStripSeparator _ToolStripSeparator4;

	[AccessedThroughProperty("MultiplyToolStripMenuItem")]
	private ToolStripMenuItem _MultiplyToolStripMenuItem;

	[AccessedThroughProperty("DivideToolStripMenuItem")]
	private ToolStripMenuItem _DivideToolStripMenuItem;

	[AccessedThroughProperty("ToolStripSeparator15")]
	private ToolStripSeparator _ToolStripSeparator15;

	[AccessedThroughProperty("ToolStripTextBox2")]
	private ToolStripTextBox _ToolStripTextBox2;

	[AccessedThroughProperty("ScaleXAxisMenuItem")]
	private ToolStripMenuItem _ScaleXAxisMenuItem;

	[AccessedThroughProperty("ScaleYAxisMenuItem")]
	private ToolStripMenuItem _ScaleYAxisMenuItem;

	[AccessedThroughProperty("ToolStripSeparator16")]
	private ToolStripSeparator _ToolStripSeparator16;

	[AccessedThroughProperty("ImportAxisMenuItem")]
	private ToolStripMenuItem _ImportAxisMenuItem;

	[AccessedThroughProperty("SelectToolStripMenuItem")]
	private ToolStripMenuItem _SelectToolStripMenuItem;

	[AccessedThroughProperty("SelectNullsToolStripMenuItem")]
	private ToolStripMenuItem _SelectNullsToolStripMenuItem;

	[AccessedThroughProperty("SelectNonNullsToolStripMenuItem")]
	private ToolStripMenuItem _SelectNonNullsToolStripMenuItem;

	[AccessedThroughProperty("SelectZerosToolStripMenuItem")]
	private ToolStripMenuItem _SelectZerosToolStripMenuItem;

	[AccessedThroughProperty("SelectNonZerosToolStripMenuItem")]
	private ToolStripMenuItem _SelectNonZerosToolStripMenuItem;

	[AccessedThroughProperty("SelectPositiveToolStripMenuItem")]
	private ToolStripMenuItem _SelectPositiveToolStripMenuItem;

	[AccessedThroughProperty("SelectNegativeToolStripMenuItem")]
	private ToolStripMenuItem _SelectNegativeToolStripMenuItem;

	private SolidBrush T_Brush;

	private Pen T_Pen;

	private SolidBrush C_Brush;

	private Pen C_Pen;

	private byte IsDrawling;

	[AccessedThroughProperty("Graph")]
	private Form _Graph;

	private byte IsDrawlingG;

	private float XD;

	private float YD;

	private float ZD;

	private float XDS;

	private float YDS;

	private float ZDS;

	private float VW_X;

	private float VW_Y;

	private float VW_Z;

	private float VW_ZM;

	private int GMB;

	private int GMX;

	private int GMY;

	private int GMD;

	private int GMSX;

	private int GMSY;

	private float GMSV;

	private float GMSS;

	private bool GMMF;

	[AccessedThroughProperty("Toolbar")]
	private Form _Toolbar;

	[AccessedThroughProperty("TB_Text1")]
	private TextBox _TB_Text1;

	[AccessedThroughProperty("TB_Btn1")]
	private Button _TB_Btn1;

	[AccessedThroughProperty("TB_Btn2")]
	private Button _TB_Btn2;

	[AccessedThroughProperty("TB_Btn3")]
	private Button _TB_Btn3;

	[AccessedThroughProperty("TB_Btn4")]
	private Button _TB_Btn4;

	[AccessedThroughProperty("TB_Btn5")]
	private Button _TB_Btn5;

	[AccessedThroughProperty("TB_Btn6")]
	private Button _TB_Btn6;

	[AccessedThroughProperty("TB_Btn7")]
	private Button _TB_Btn7;

	[AccessedThroughProperty("TB_Btn8")]
	private Button _TB_Btn8;

	[AccessedThroughProperty("TB_Btn9")]
	private Button _TB_Btn9;

	[AccessedThroughProperty("TB_Btn10")]
	private Button _TB_Btn10;

	[AccessedThroughProperty("TB_Btn11")]
	private Button _TB_Btn11;

	[AccessedThroughProperty("TB_Btn12")]
	private Button _TB_Btn12;

	[AccessedThroughProperty("TB_Btn13")]
	private Button _TB_Btn13;

	[AccessedThroughProperty("TB_Timer1")]
	private Timer _TB_Timer1;

	private float VW_CX;

	private float VW_CY;

	private int GMCX;

	private int GMCY;

	private byte Mouse_Over;

	private byte Mouse_OverP;

	private byte DFocus;

	private byte DFocusP;

	private int MAX_X;

	private int MAX_Y;

	private int MAX_U;

	public float[] GData;

	public byte[] SData;

	private float[] GDataU;

	private int Busy;

	private byte UndoC;

	private byte Init;

	private string m_Grid_VisibleName;

	private int m_Grid_X;

	private int m_Grid_Y;

	private byte m_Grid_ShowLabels;

	private byte m_Grid_Transpose;

	private byte m_Grid_TransposeCopyPaste;

	private byte m_Grid_GraphType;

	private byte m_Grid_ReDraw;

	private byte m_Grid_FreezeDraw;

	private int m_Grid_AxisStatus;

	private int m_Grid_DataStatus;

	private float m_Grid_DataOffset;

	private float m_Grid_DataScalar;

	private byte m_Grid_DataSCopyPaste;

	private int m_Cell_W;

	private int m_Cell_H;

	private byte m_Cell_Auto_W;

	private byte m_Cell_ShowChanges;

	private byte m_Cell_CharMax;

	private string m_Cell_Format;

	private string m_Cell_LabelFormat;

	private string m_Cell_CPFormat;

	private Color m_Cell_LowCLR;

	private Color m_Cell_HighCLR;

	private Color m_Cell_FontCLR;

	private Color m_Cell_LSelCLR;

	private Color m_Cell_HSelCLR;

	private Color m_Cell_FSelCLR;

	private int MultiSelect;

	private byte ControlButton;

	private int LX;

	private int LY;

	private int L2X;

	private int L2Y;

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
			//IL_0016: Unknown result type (might be due to invalid IL or missing references)
			//IL_001c: Expected O, but got Unknown
			EventHandler eventHandler = TextBox1_LostFocus;
			KeyPressEventHandler val = new KeyPressEventHandler(TextBox1_KeyPress);
			if (_TextBox1 != null)
			{
				((Control)_TextBox1).LostFocus -= eventHandler;
				((Control)_TextBox1).KeyPress -= val;
			}
			_TextBox1 = value;
			if (_TextBox1 != null)
			{
				((Control)_TextBox1).LostFocus += eventHandler;
				((Control)_TextBox1).KeyPress += val;
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

	internal virtual ContextMenuStrip DataMenuStrip
	{
		[DebuggerNonUserCode]
		get
		{
			return _DataMenuStrip;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			CancelEventHandler cancelEventHandler = DataMenuStrip_Opening;
			if (_DataMenuStrip != null)
			{
				((ToolStripDropDown)_DataMenuStrip).Opening -= cancelEventHandler;
			}
			_DataMenuStrip = value;
			if (_DataMenuStrip != null)
			{
				((ToolStripDropDown)_DataMenuStrip).Opening += cancelEventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem CopyToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _CopyToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = CopyToolStripMenuItem_Click;
			if (_CopyToolStripMenuItem != null)
			{
				((ToolStripItem)_CopyToolStripMenuItem).Click -= eventHandler;
			}
			_CopyToolStripMenuItem = value;
			if (_CopyToolStripMenuItem != null)
			{
				((ToolStripItem)_CopyToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem PasteToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _PasteToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = PasteToolStripMenuItem_Click;
			if (_PasteToolStripMenuItem != null)
			{
				((ToolStripItem)_PasteToolStripMenuItem).Click -= eventHandler;
			}
			_PasteToolStripMenuItem = value;
			if (_PasteToolStripMenuItem != null)
			{
				((ToolStripItem)_PasteToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem ManipulateToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _ManipulateToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = ManipulateToolStripMenuItem_Click;
			if (_ManipulateToolStripMenuItem != null)
			{
				((ToolStripItem)_ManipulateToolStripMenuItem).Click -= eventHandler;
			}
			_ManipulateToolStripMenuItem = value;
			if (_ManipulateToolStripMenuItem != null)
			{
				((ToolStripItem)_ManipulateToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem GraphToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _GraphToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = GraphToolStripMenuItem_Click;
			if (_GraphToolStripMenuItem != null)
			{
				((ToolStripItem)_GraphToolStripMenuItem).Click -= eventHandler;
			}
			_GraphToolStripMenuItem = value;
			if (_GraphToolStripMenuItem != null)
			{
				((ToolStripItem)_GraphToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem CopyLabelsToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _CopyLabelsToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = CopyLabelsToolStripMenuItem_Click;
			if (_CopyLabelsToolStripMenuItem != null)
			{
				((ToolStripItem)_CopyLabelsToolStripMenuItem).Click -= eventHandler;
			}
			_CopyLabelsToolStripMenuItem = value;
			if (_CopyLabelsToolStripMenuItem != null)
			{
				((ToolStripItem)_CopyLabelsToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem PasteLabelsToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _PasteLabelsToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = PasteLabelsToolStripMenuItem_Click;
			if (_PasteLabelsToolStripMenuItem != null)
			{
				((ToolStripItem)_PasteLabelsToolStripMenuItem).Click -= eventHandler;
			}
			_PasteLabelsToolStripMenuItem = value;
			if (_PasteLabelsToolStripMenuItem != null)
			{
				((ToolStripItem)_PasteLabelsToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem PasteLabelsInterpolateToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _PasteLabelsInterpolateToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = PasteLabelsInterpolateToolStripMenuItem_Click;
			if (_PasteLabelsInterpolateToolStripMenuItem != null)
			{
				((ToolStripItem)_PasteLabelsInterpolateToolStripMenuItem).Click -= eventHandler;
			}
			_PasteLabelsInterpolateToolStripMenuItem = value;
			if (_PasteLabelsInterpolateToolStripMenuItem != null)
			{
				((ToolStripItem)_PasteLabelsInterpolateToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem PasteAddToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _PasteAddToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = PasteAddToolStripMenuItem_Click;
			if (_PasteAddToolStripMenuItem != null)
			{
				((ToolStripItem)_PasteAddToolStripMenuItem).Click -= eventHandler;
			}
			_PasteAddToolStripMenuItem = value;
			if (_PasteAddToolStripMenuItem != null)
			{
				((ToolStripItem)_PasteAddToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem PasteSubtractToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _PasteSubtractToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = PasteSubtractToolStripMenuItem_Click;
			if (_PasteSubtractToolStripMenuItem != null)
			{
				((ToolStripItem)_PasteSubtractToolStripMenuItem).Click -= eventHandler;
			}
			_PasteSubtractToolStripMenuItem = value;
			if (_PasteSubtractToolStripMenuItem != null)
			{
				((ToolStripItem)_PasteSubtractToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem PasteMultiplyToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _PasteMultiplyToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = PasteMultiplyToolStripMenuItem_Click;
			if (_PasteMultiplyToolStripMenuItem != null)
			{
				((ToolStripItem)_PasteMultiplyToolStripMenuItem).Click -= eventHandler;
			}
			_PasteMultiplyToolStripMenuItem = value;
			if (_PasteMultiplyToolStripMenuItem != null)
			{
				((ToolStripItem)_PasteMultiplyToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem PasteMultiplyPctToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _PasteMultiplyPctToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = PasteMultiplyPctToolStripMenuItem_Click;
			if (_PasteMultiplyPctToolStripMenuItem != null)
			{
				((ToolStripItem)_PasteMultiplyPctToolStripMenuItem).Click -= eventHandler;
			}
			_PasteMultiplyPctToolStripMenuItem = value;
			if (_PasteMultiplyPctToolStripMenuItem != null)
			{
				((ToolStripItem)_PasteMultiplyPctToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem PasteMultiplyPctHalfToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _PasteMultiplyPctHalfToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = PasteMultiplyPctHalfToolStripMenuItem_Click;
			if (_PasteMultiplyPctHalfToolStripMenuItem != null)
			{
				((ToolStripItem)_PasteMultiplyPctHalfToolStripMenuItem).Click -= eventHandler;
			}
			_PasteMultiplyPctHalfToolStripMenuItem = value;
			if (_PasteMultiplyPctHalfToolStripMenuItem != null)
			{
				((ToolStripItem)_PasteMultiplyPctHalfToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem PasteDivideToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _PasteDivideToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = PasteDivideToolStripMenuItem_Click;
			if (_PasteDivideToolStripMenuItem != null)
			{
				((ToolStripItem)_PasteDivideToolStripMenuItem).Click -= eventHandler;
			}
			_PasteDivideToolStripMenuItem = value;
			if (_PasteDivideToolStripMenuItem != null)
			{
				((ToolStripItem)_PasteDivideToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem PasteAverageToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _PasteAverageToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = PasteAverageToolStripMenuItem_Click;
			if (_PasteAverageToolStripMenuItem != null)
			{
				((ToolStripItem)_PasteAverageToolStripMenuItem).Click -= eventHandler;
			}
			_PasteAverageToolStripMenuItem = value;
			if (_PasteAverageToolStripMenuItem != null)
			{
				((ToolStripItem)_PasteAverageToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem SmoothToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _SmoothToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = SmoothToolStripMenuItem_Click;
			if (_SmoothToolStripMenuItem != null)
			{
				((ToolStripItem)_SmoothToolStripMenuItem).Click -= eventHandler;
			}
			_SmoothToolStripMenuItem = value;
			if (_SmoothToolStripMenuItem != null)
			{
				((ToolStripItem)_SmoothToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem SmoothHorizontalToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _SmoothHorizontalToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = SmoothHorizontalToolStripMenuItem_Click;
			if (_SmoothHorizontalToolStripMenuItem != null)
			{
				((ToolStripItem)_SmoothHorizontalToolStripMenuItem).Click -= eventHandler;
			}
			_SmoothHorizontalToolStripMenuItem = value;
			if (_SmoothHorizontalToolStripMenuItem != null)
			{
				((ToolStripItem)_SmoothHorizontalToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem SmoothVerticalToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _SmoothVerticalToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = SmoothVerticalToolStripMenuItem_Click;
			if (_SmoothVerticalToolStripMenuItem != null)
			{
				((ToolStripItem)_SmoothVerticalToolStripMenuItem).Click -= eventHandler;
			}
			_SmoothVerticalToolStripMenuItem = value;
			if (_SmoothVerticalToolStripMenuItem != null)
			{
				((ToolStripItem)_SmoothVerticalToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem InterpolateToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _InterpolateToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = InterpolateToolStripMenuItem_Click;
			if (_InterpolateToolStripMenuItem != null)
			{
				((ToolStripItem)_InterpolateToolStripMenuItem).Click -= eventHandler;
			}
			_InterpolateToolStripMenuItem = value;
			if (_InterpolateToolStripMenuItem != null)
			{
				((ToolStripItem)_InterpolateToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem InterpolateHorizontalToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _InterpolateHorizontalToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = InterpolateHorizontalToolStripMenuItem_Click;
			if (_InterpolateHorizontalToolStripMenuItem != null)
			{
				((ToolStripItem)_InterpolateHorizontalToolStripMenuItem).Click -= eventHandler;
			}
			_InterpolateHorizontalToolStripMenuItem = value;
			if (_InterpolateHorizontalToolStripMenuItem != null)
			{
				((ToolStripItem)_InterpolateHorizontalToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem InterpolateVerticalToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _InterpolateVerticalToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = InterpolateVerticalToolStripMenuItem_Click;
			if (_InterpolateVerticalToolStripMenuItem != null)
			{
				((ToolStripItem)_InterpolateVerticalToolStripMenuItem).Click -= eventHandler;
			}
			_InterpolateVerticalToolStripMenuItem = value;
			if (_InterpolateVerticalToolStripMenuItem != null)
			{
				((ToolStripItem)_InterpolateVerticalToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem ExtrapolateToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _ExtrapolateToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = ExtrapolateToolStripMenuItem_Click;
			if (_ExtrapolateToolStripMenuItem != null)
			{
				((ToolStripItem)_ExtrapolateToolStripMenuItem).Click -= eventHandler;
			}
			_ExtrapolateToolStripMenuItem = value;
			if (_ExtrapolateToolStripMenuItem != null)
			{
				((ToolStripItem)_ExtrapolateToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem Graph2DToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _Graph2DToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = Graph2DToolStripMenuItem_Click;
			if (_Graph2DToolStripMenuItem != null)
			{
				((ToolStripItem)_Graph2DToolStripMenuItem).Click -= eventHandler;
			}
			_Graph2DToolStripMenuItem = value;
			if (_Graph2DToolStripMenuItem != null)
			{
				((ToolStripItem)_Graph2DToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem Graph3DToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _Graph3DToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = Graph3DToolStripMenuItem_Click;
			if (_Graph3DToolStripMenuItem != null)
			{
				((ToolStripItem)_Graph3DToolStripMenuItem).Click -= eventHandler;
			}
			_Graph3DToolStripMenuItem = value;
			if (_Graph3DToolStripMenuItem != null)
			{
				((ToolStripItem)_Graph3DToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem ToolbarToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _ToolbarToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = ToolbarToolStripMenuItem_Click;
			if (_ToolbarToolStripMenuItem != null)
			{
				((ToolStripItem)_ToolbarToolStripMenuItem).Click -= eventHandler;
			}
			_ToolbarToolStripMenuItem = value;
			if (_ToolbarToolStripMenuItem != null)
			{
				((ToolStripItem)_ToolbarToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripSeparator ToolStripSeparator2
	{
		[DebuggerNonUserCode]
		get
		{
			return _ToolStripSeparator2;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_ToolStripSeparator2 = value;
		}
	}

	internal virtual ToolStripSeparator ToolStripSeparator1
	{
		[DebuggerNonUserCode]
		get
		{
			return _ToolStripSeparator1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_ToolStripSeparator1 = value;
		}
	}

	internal virtual ToolStripMenuItem UndoToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _UndoToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = UndoToolStripMenuItem_Click;
			if (_UndoToolStripMenuItem != null)
			{
				((ToolStripItem)_UndoToolStripMenuItem).Click -= eventHandler;
			}
			_UndoToolStripMenuItem = value;
			if (_UndoToolStripMenuItem != null)
			{
				((ToolStripItem)_UndoToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripSeparator ToolStripSeparator7
	{
		[DebuggerNonUserCode]
		get
		{
			return _ToolStripSeparator7;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_ToolStripSeparator7 = value;
		}
	}

	internal virtual ToolStripSeparator ToolStripSeparator8
	{
		[DebuggerNonUserCode]
		get
		{
			return _ToolStripSeparator8;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_ToolStripSeparator8 = value;
		}
	}

	internal virtual ToolStripSeparator ToolStripSeparator9
	{
		[DebuggerNonUserCode]
		get
		{
			return _ToolStripSeparator9;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_ToolStripSeparator9 = value;
		}
	}

	internal virtual ToolStripSeparator ToolStripSeparator10
	{
		[DebuggerNonUserCode]
		get
		{
			return _ToolStripSeparator10;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_ToolStripSeparator10 = value;
		}
	}

	internal virtual ToolStripSeparator ToolStripSeparator5
	{
		[DebuggerNonUserCode]
		get
		{
			return _ToolStripSeparator5;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_ToolStripSeparator5 = value;
		}
	}

	internal virtual ToolStripSeparator ToolStripSeparator6
	{
		[DebuggerNonUserCode]
		get
		{
			return _ToolStripSeparator6;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_ToolStripSeparator6 = value;
		}
	}

	internal virtual ToolStripMenuItem OtherMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _OtherMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_OtherMenuItem = value;
		}
	}

	internal virtual ToolStripMenuItem TransposeClipboardToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _TransposeClipboardToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = TransposeClipboardToolStripMenuItem_Click;
			if (_TransposeClipboardToolStripMenuItem != null)
			{
				((ToolStripItem)_TransposeClipboardToolStripMenuItem).Click -= eventHandler;
			}
			_TransposeClipboardToolStripMenuItem = value;
			if (_TransposeClipboardToolStripMenuItem != null)
			{
				((ToolStripItem)_TransposeClipboardToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem ClearChangedFlagToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _ClearChangedFlagToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = ClearChangedFlagToolStripMenuItem_Click;
			if (_ClearChangedFlagToolStripMenuItem != null)
			{
				((ToolStripItem)_ClearChangedFlagToolStripMenuItem).Click -= eventHandler;
			}
			_ClearChangedFlagToolStripMenuItem = value;
			if (_ClearChangedFlagToolStripMenuItem != null)
			{
				((ToolStripItem)_ClearChangedFlagToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripSeparator ToolStripSeparator11
	{
		[DebuggerNonUserCode]
		get
		{
			return _ToolStripSeparator11;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_ToolStripSeparator11 = value;
		}
	}

	internal virtual ToolStripMenuItem ToggleChangeFlagDisplayToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _ToggleChangeFlagDisplayToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = ToggleChangeFlagDisplayToolStripMenuItem_Click;
			if (_ToggleChangeFlagDisplayToolStripMenuItem != null)
			{
				((ToolStripItem)_ToggleChangeFlagDisplayToolStripMenuItem).Click -= eventHandler;
			}
			_ToggleChangeFlagDisplayToolStripMenuItem = value;
			if (_ToggleChangeFlagDisplayToolStripMenuItem != null)
			{
				((ToolStripItem)_ToggleChangeFlagDisplayToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripSeparator ToolStripSeparator12
	{
		[DebuggerNonUserCode]
		get
		{
			return _ToolStripSeparator12;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_ToolStripSeparator12 = value;
		}
	}

	internal virtual ToolStripMenuItem ClearTableToZerosToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _ClearTableToZerosToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = ClearTableToZerosToolStripMenuItem_Click;
			if (_ClearTableToZerosToolStripMenuItem != null)
			{
				((ToolStripItem)_ClearTableToZerosToolStripMenuItem).Click -= eventHandler;
			}
			_ClearTableToZerosToolStripMenuItem = value;
			if (_ClearTableToZerosToolStripMenuItem != null)
			{
				((ToolStripItem)_ClearTableToZerosToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem ClearTableToNullsToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _ClearTableToNullsToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = ClearTableToNullsToolStripMenuItem_Click;
			if (_ClearTableToNullsToolStripMenuItem != null)
			{
				((ToolStripItem)_ClearTableToNullsToolStripMenuItem).Click -= eventHandler;
			}
			_ClearTableToNullsToolStripMenuItem = value;
			if (_ClearTableToNullsToolStripMenuItem != null)
			{
				((ToolStripItem)_ClearTableToNullsToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripSeparator ToolStripSeparator13
	{
		[DebuggerNonUserCode]
		get
		{
			return _ToolStripSeparator13;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_ToolStripSeparator13 = value;
		}
	}

	internal virtual ToolStripMenuItem ConvertZerosToNullsToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _ConvertZerosToNullsToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = ConvertZerosToNullsToolStripMenuItem_Click;
			if (_ConvertZerosToNullsToolStripMenuItem != null)
			{
				((ToolStripItem)_ConvertZerosToNullsToolStripMenuItem).Click -= eventHandler;
			}
			_ConvertZerosToNullsToolStripMenuItem = value;
			if (_ConvertZerosToNullsToolStripMenuItem != null)
			{
				((ToolStripItem)_ConvertZerosToNullsToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem ConvertNullsToZerosToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _ConvertNullsToZerosToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = ConvertNullsToZerosToolStripMenuItem_Click;
			if (_ConvertNullsToZerosToolStripMenuItem != null)
			{
				((ToolStripItem)_ConvertNullsToZerosToolStripMenuItem).Click -= eventHandler;
			}
			_ConvertNullsToZerosToolStripMenuItem = value;
			if (_ConvertNullsToZerosToolStripMenuItem != null)
			{
				((ToolStripItem)_ConvertNullsToZerosToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripSeparator ToolStripSeparator14
	{
		[DebuggerNonUserCode]
		get
		{
			return _ToolStripSeparator14;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_ToolStripSeparator14 = value;
		}
	}

	internal virtual ToolStripMenuItem EditToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _EditToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = EditToolStripMenuItem_Click;
			if (_EditToolStripMenuItem != null)
			{
				((ToolStripItem)_EditToolStripMenuItem).Click -= eventHandler;
			}
			_EditToolStripMenuItem = value;
			if (_EditToolStripMenuItem != null)
			{
				((ToolStripItem)_EditToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripTextBox ToolStripTextBox1
	{
		[DebuggerNonUserCode]
		get
		{
			return _ToolStripTextBox1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_ToolStripTextBox1 = value;
		}
	}

	internal virtual ToolStripMenuItem FillToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _FillToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = FillToolStripMenuItem_Click;
			if (_FillToolStripMenuItem != null)
			{
				((ToolStripItem)_FillToolStripMenuItem).Click -= eventHandler;
			}
			_FillToolStripMenuItem = value;
			if (_FillToolStripMenuItem != null)
			{
				((ToolStripItem)_FillToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripSeparator ToolStripSeparator3
	{
		[DebuggerNonUserCode]
		get
		{
			return _ToolStripSeparator3;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_ToolStripSeparator3 = value;
		}
	}

	internal virtual ToolStripMenuItem AddToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _AddToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = AddToolStripMenuItem_Click;
			if (_AddToolStripMenuItem != null)
			{
				((ToolStripItem)_AddToolStripMenuItem).Click -= eventHandler;
			}
			_AddToolStripMenuItem = value;
			if (_AddToolStripMenuItem != null)
			{
				((ToolStripItem)_AddToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem SubtractToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _SubtractToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = SubtractToolStripMenuItem_Click;
			if (_SubtractToolStripMenuItem != null)
			{
				((ToolStripItem)_SubtractToolStripMenuItem).Click -= eventHandler;
			}
			_SubtractToolStripMenuItem = value;
			if (_SubtractToolStripMenuItem != null)
			{
				((ToolStripItem)_SubtractToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripSeparator ToolStripSeparator4
	{
		[DebuggerNonUserCode]
		get
		{
			return _ToolStripSeparator4;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_ToolStripSeparator4 = value;
		}
	}

	internal virtual ToolStripMenuItem MultiplyToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _MultiplyToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = MultiplyToolStripMenuItem_Click;
			if (_MultiplyToolStripMenuItem != null)
			{
				((ToolStripItem)_MultiplyToolStripMenuItem).Click -= eventHandler;
			}
			_MultiplyToolStripMenuItem = value;
			if (_MultiplyToolStripMenuItem != null)
			{
				((ToolStripItem)_MultiplyToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem DivideToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _DivideToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = DivideToolStripMenuItem_Click;
			if (_DivideToolStripMenuItem != null)
			{
				((ToolStripItem)_DivideToolStripMenuItem).Click -= eventHandler;
			}
			_DivideToolStripMenuItem = value;
			if (_DivideToolStripMenuItem != null)
			{
				((ToolStripItem)_DivideToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripSeparator ToolStripSeparator15
	{
		[DebuggerNonUserCode]
		get
		{
			return _ToolStripSeparator15;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_ToolStripSeparator15 = value;
		}
	}

	internal virtual ToolStripTextBox ToolStripTextBox2
	{
		[DebuggerNonUserCode]
		get
		{
			return _ToolStripTextBox2;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_ToolStripTextBox2 = value;
		}
	}

	internal virtual ToolStripMenuItem ScaleXAxisMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _ScaleXAxisMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = ScaleXAxisMenuItem_Click;
			if (_ScaleXAxisMenuItem != null)
			{
				((ToolStripItem)_ScaleXAxisMenuItem).Click -= eventHandler;
			}
			_ScaleXAxisMenuItem = value;
			if (_ScaleXAxisMenuItem != null)
			{
				((ToolStripItem)_ScaleXAxisMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem ScaleYAxisMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _ScaleYAxisMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = ScaleYAxisMenuItem_Click;
			if (_ScaleYAxisMenuItem != null)
			{
				((ToolStripItem)_ScaleYAxisMenuItem).Click -= eventHandler;
			}
			_ScaleYAxisMenuItem = value;
			if (_ScaleYAxisMenuItem != null)
			{
				((ToolStripItem)_ScaleYAxisMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripSeparator ToolStripSeparator16
	{
		[DebuggerNonUserCode]
		get
		{
			return _ToolStripSeparator16;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_ToolStripSeparator16 = value;
		}
	}

	internal virtual ToolStripMenuItem ImportAxisMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _ImportAxisMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = ImportAxisMenuItem_Click;
			if (_ImportAxisMenuItem != null)
			{
				((ToolStripItem)_ImportAxisMenuItem).Click -= eventHandler;
			}
			_ImportAxisMenuItem = value;
			if (_ImportAxisMenuItem != null)
			{
				((ToolStripItem)_ImportAxisMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem SelectToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _SelectToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_SelectToolStripMenuItem = value;
		}
	}

	internal virtual ToolStripMenuItem SelectNullsToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _SelectNullsToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = SelectNullsToolStripMenuItem_Click;
			if (_SelectNullsToolStripMenuItem != null)
			{
				((ToolStripItem)_SelectNullsToolStripMenuItem).Click -= eventHandler;
			}
			_SelectNullsToolStripMenuItem = value;
			if (_SelectNullsToolStripMenuItem != null)
			{
				((ToolStripItem)_SelectNullsToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem SelectNonNullsToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _SelectNonNullsToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = SelectNonNullsToolStripMenuItem_Click;
			if (_SelectNonNullsToolStripMenuItem != null)
			{
				((ToolStripItem)_SelectNonNullsToolStripMenuItem).Click -= eventHandler;
			}
			_SelectNonNullsToolStripMenuItem = value;
			if (_SelectNonNullsToolStripMenuItem != null)
			{
				((ToolStripItem)_SelectNonNullsToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem SelectZerosToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _SelectZerosToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = SelectZerosToolStripMenuItem_Click;
			if (_SelectZerosToolStripMenuItem != null)
			{
				((ToolStripItem)_SelectZerosToolStripMenuItem).Click -= eventHandler;
			}
			_SelectZerosToolStripMenuItem = value;
			if (_SelectZerosToolStripMenuItem != null)
			{
				((ToolStripItem)_SelectZerosToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem SelectNonZerosToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _SelectNonZerosToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = SelectNonZerosToolStripMenuItem_Click;
			if (_SelectNonZerosToolStripMenuItem != null)
			{
				((ToolStripItem)_SelectNonZerosToolStripMenuItem).Click -= eventHandler;
			}
			_SelectNonZerosToolStripMenuItem = value;
			if (_SelectNonZerosToolStripMenuItem != null)
			{
				((ToolStripItem)_SelectNonZerosToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem SelectPositiveToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _SelectPositiveToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = SelectPositiveToolStripMenuItem_Click;
			if (_SelectPositiveToolStripMenuItem != null)
			{
				((ToolStripItem)_SelectPositiveToolStripMenuItem).Click -= eventHandler;
			}
			_SelectPositiveToolStripMenuItem = value;
			if (_SelectPositiveToolStripMenuItem != null)
			{
				((ToolStripItem)_SelectPositiveToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem SelectNegativeToolStripMenuItem
	{
		[DebuggerNonUserCode]
		get
		{
			return _SelectNegativeToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = SelectNegativeToolStripMenuItem_Click;
			if (_SelectNegativeToolStripMenuItem != null)
			{
				((ToolStripItem)_SelectNegativeToolStripMenuItem).Click -= eventHandler;
			}
			_SelectNegativeToolStripMenuItem = value;
			if (_SelectNegativeToolStripMenuItem != null)
			{
				((ToolStripItem)_SelectNegativeToolStripMenuItem).Click += eventHandler;
			}
		}
	}

	internal virtual Form Graph
	{
		[DebuggerNonUserCode]
		get
		{
			return _Graph;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			//IL_0008: Unknown result type (might be due to invalid IL or missing references)
			//IL_000e: Expected O, but got Unknown
			//IL_0016: Unknown result type (might be due to invalid IL or missing references)
			//IL_001c: Expected O, but got Unknown
			//IL_0024: Unknown result type (might be due to invalid IL or missing references)
			//IL_002a: Expected O, but got Unknown
			//IL_0032: Unknown result type (might be due to invalid IL or missing references)
			//IL_0038: Expected O, but got Unknown
			//IL_007c: Unknown result type (might be due to invalid IL or missing references)
			//IL_0083: Expected O, but got Unknown
			MouseEventHandler val = new MouseEventHandler(Graph_MouseWheel);
			MouseEventHandler val2 = new MouseEventHandler(Graph_MouseDown);
			MouseEventHandler val3 = new MouseEventHandler(Graph_MouseUp);
			MouseEventHandler val4 = new MouseEventHandler(Graph_MouseMove);
			EventHandler eventHandler = Graph_MouseLeave;
			EventHandler eventHandler2 = Graph_MouseEnter;
			CancelEventHandler cancelEventHandler = Graph_Closing;
			EventHandler eventHandler3 = [SpecialName] [DebuggerStepThrough] (object a0, EventArgs a1) =>
			{
				Graph_Resize();
			};
			PaintEventHandler val5 = new PaintEventHandler(Graph_Paint);
			if (_Graph != null)
			{
				((Control)_Graph).MouseWheel -= val;
				((Control)_Graph).MouseDown -= val2;
				((Control)_Graph).MouseUp -= val3;
				((Control)_Graph).MouseMove -= val4;
				((Control)_Graph).MouseLeave -= eventHandler;
				((Control)_Graph).MouseEnter -= eventHandler2;
				_Graph.Closing -= cancelEventHandler;
				((Control)_Graph).Resize -= eventHandler3;
				((Control)_Graph).Paint -= val5;
			}
			_Graph = value;
			if (_Graph != null)
			{
				((Control)_Graph).MouseWheel += val;
				((Control)_Graph).MouseDown += val2;
				((Control)_Graph).MouseUp += val3;
				((Control)_Graph).MouseMove += val4;
				((Control)_Graph).MouseLeave += eventHandler;
				((Control)_Graph).MouseEnter += eventHandler2;
				_Graph.Closing += cancelEventHandler;
				((Control)_Graph).Resize += eventHandler3;
				((Control)_Graph).Paint += val5;
			}
		}
	}

	internal virtual Form Toolbar
	{
		[DebuggerNonUserCode]
		get
		{
			return _Toolbar;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			CancelEventHandler cancelEventHandler = Toolbar_Closing;
			if (_Toolbar != null)
			{
				_Toolbar.Closing -= cancelEventHandler;
			}
			_Toolbar = value;
			if (_Toolbar != null)
			{
				_Toolbar.Closing += cancelEventHandler;
			}
		}
	}

	internal virtual TextBox TB_Text1
	{
		[DebuggerNonUserCode]
		get
		{
			return _TB_Text1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			//IL_0008: Unknown result type (might be due to invalid IL or missing references)
			//IL_000e: Expected O, but got Unknown
			KeyPressEventHandler val = new KeyPressEventHandler(TB_Text1_KeyPress);
			if (_TB_Text1 != null)
			{
				((Control)_TB_Text1).KeyPress -= val;
			}
			_TB_Text1 = value;
			if (_TB_Text1 != null)
			{
				((Control)_TB_Text1).KeyPress += val;
			}
		}
	}

	internal virtual Button TB_Btn1
	{
		[DebuggerNonUserCode]
		get
		{
			return _TB_Btn1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = TB_Btn1_Click;
			if (_TB_Btn1 != null)
			{
				((Control)_TB_Btn1).Click -= eventHandler;
			}
			_TB_Btn1 = value;
			if (_TB_Btn1 != null)
			{
				((Control)_TB_Btn1).Click += eventHandler;
			}
		}
	}

	internal virtual Button TB_Btn2
	{
		[DebuggerNonUserCode]
		get
		{
			return _TB_Btn2;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = TB_Btn2_Click;
			if (_TB_Btn2 != null)
			{
				((Control)_TB_Btn2).Click -= eventHandler;
			}
			_TB_Btn2 = value;
			if (_TB_Btn2 != null)
			{
				((Control)_TB_Btn2).Click += eventHandler;
			}
		}
	}

	internal virtual Button TB_Btn3
	{
		[DebuggerNonUserCode]
		get
		{
			return _TB_Btn3;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = TB_Btn3_Click;
			if (_TB_Btn3 != null)
			{
				((Control)_TB_Btn3).Click -= eventHandler;
			}
			_TB_Btn3 = value;
			if (_TB_Btn3 != null)
			{
				((Control)_TB_Btn3).Click += eventHandler;
			}
		}
	}

	internal virtual Button TB_Btn4
	{
		[DebuggerNonUserCode]
		get
		{
			return _TB_Btn4;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = TB_Btn4_Click;
			if (_TB_Btn4 != null)
			{
				((Control)_TB_Btn4).Click -= eventHandler;
			}
			_TB_Btn4 = value;
			if (_TB_Btn4 != null)
			{
				((Control)_TB_Btn4).Click += eventHandler;
			}
		}
	}

	internal virtual Button TB_Btn5
	{
		[DebuggerNonUserCode]
		get
		{
			return _TB_Btn5;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = TB_Btn5_Click;
			if (_TB_Btn5 != null)
			{
				((Control)_TB_Btn5).Click -= eventHandler;
			}
			_TB_Btn5 = value;
			if (_TB_Btn5 != null)
			{
				((Control)_TB_Btn5).Click += eventHandler;
			}
		}
	}

	internal virtual Button TB_Btn6
	{
		[DebuggerNonUserCode]
		get
		{
			return _TB_Btn6;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = TB_Btn6_Click;
			if (_TB_Btn6 != null)
			{
				((Control)_TB_Btn6).Click -= eventHandler;
			}
			_TB_Btn6 = value;
			if (_TB_Btn6 != null)
			{
				((Control)_TB_Btn6).Click += eventHandler;
			}
		}
	}

	internal virtual Button TB_Btn7
	{
		[DebuggerNonUserCode]
		get
		{
			return _TB_Btn7;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = TB_Btn7_Click;
			if (_TB_Btn7 != null)
			{
				((Control)_TB_Btn7).Click -= eventHandler;
			}
			_TB_Btn7 = value;
			if (_TB_Btn7 != null)
			{
				((Control)_TB_Btn7).Click += eventHandler;
			}
		}
	}

	internal virtual Button TB_Btn8
	{
		[DebuggerNonUserCode]
		get
		{
			return _TB_Btn8;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = TB_Btn8_Click;
			if (_TB_Btn8 != null)
			{
				((Control)_TB_Btn8).Click -= eventHandler;
			}
			_TB_Btn8 = value;
			if (_TB_Btn8 != null)
			{
				((Control)_TB_Btn8).Click += eventHandler;
			}
		}
	}

	internal virtual Button TB_Btn9
	{
		[DebuggerNonUserCode]
		get
		{
			return _TB_Btn9;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = TB_Btn9_Click;
			if (_TB_Btn9 != null)
			{
				((Control)_TB_Btn9).Click -= eventHandler;
			}
			_TB_Btn9 = value;
			if (_TB_Btn9 != null)
			{
				((Control)_TB_Btn9).Click += eventHandler;
			}
		}
	}

	internal virtual Button TB_Btn10
	{
		[DebuggerNonUserCode]
		get
		{
			return _TB_Btn10;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = TB_Btn10_Click;
			if (_TB_Btn10 != null)
			{
				((Control)_TB_Btn10).Click -= eventHandler;
			}
			_TB_Btn10 = value;
			if (_TB_Btn10 != null)
			{
				((Control)_TB_Btn10).Click += eventHandler;
			}
		}
	}

	internal virtual Button TB_Btn11
	{
		[DebuggerNonUserCode]
		get
		{
			return _TB_Btn11;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = TB_Btn11_Click;
			if (_TB_Btn11 != null)
			{
				((Control)_TB_Btn11).Click -= eventHandler;
			}
			_TB_Btn11 = value;
			if (_TB_Btn11 != null)
			{
				((Control)_TB_Btn11).Click += eventHandler;
			}
		}
	}

	internal virtual Button TB_Btn12
	{
		[DebuggerNonUserCode]
		get
		{
			return _TB_Btn12;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = TB_Btn12_Click;
			if (_TB_Btn12 != null)
			{
				((Control)_TB_Btn12).Click -= eventHandler;
			}
			_TB_Btn12 = value;
			if (_TB_Btn12 != null)
			{
				((Control)_TB_Btn12).Click += eventHandler;
			}
		}
	}

	internal virtual Button TB_Btn13
	{
		[DebuggerNonUserCode]
		get
		{
			return _TB_Btn13;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			EventHandler eventHandler = TB_Btn13_Click;
			if (_TB_Btn13 != null)
			{
				((Control)_TB_Btn13).Click -= eventHandler;
			}
			_TB_Btn13 = value;
			if (_TB_Btn13 != null)
			{
				((Control)_TB_Btn13).Click += eventHandler;
			}
		}
	}

	internal virtual Timer TB_Timer1
	{
		[DebuggerNonUserCode]
		get
		{
			return _TB_Timer1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[DebuggerNonUserCode]
		set
		{
			_TB_Timer1 = value;
		}
	}

	public string Grid_VisibleName
	{
		get
		{
			return m_Grid_VisibleName;
		}
		set
		{
			m_Grid_VisibleName = value;
		}
	}

	public int Grid_X
	{
		get
		{
			return m_Grid_X;
		}
		set
		{
			checked
			{
				if (Init == 1)
				{
					Wait();
					Busy++;
					float[,] array = new float[MAX_X + 1 + 1, MAX_Y + 1 + 1];
					int grid_X = m_Grid_X;
					for (int i = 0; i <= grid_X; i++)
					{
						int grid_Y = m_Grid_Y;
						for (int j = 0; j <= grid_Y; j++)
						{
							array[i, j] = R_Data((byte)i, (byte)j);
						}
					}
					m_Grid_X = value;
					ReSize_Data();
					int grid_X2 = m_Grid_X;
					for (int k = 0; k <= grid_X2; k++)
					{
						int grid_Y2 = m_Grid_Y;
						for (int l = 0; l <= grid_Y2; l++)
						{
							W_Data((byte)k, (byte)l, array[k, l]);
						}
					}
					ClearUndo();
					Busy--;
					if (Busy < 0)
					{
						Busy = 0;
					}
				}
				else
				{
					m_Grid_X = value;
				}
			}
		}
	}

	public int Grid_Y
	{
		get
		{
			return m_Grid_Y;
		}
		set
		{
			checked
			{
				if (Init == 1)
				{
					Wait();
					Busy++;
					float[,] array = new float[MAX_X + 1 + 1, MAX_Y + 1 + 1];
					int grid_X = m_Grid_X;
					for (int i = 0; i <= grid_X; i++)
					{
						int grid_Y = m_Grid_Y;
						for (int j = 0; j <= grid_Y; j++)
						{
							array[i, j] = R_Data((byte)i, (byte)j);
						}
					}
					m_Grid_Y = value;
					ReSize_Data();
					int grid_X2 = m_Grid_X;
					for (int k = 0; k <= grid_X2; k++)
					{
						int grid_Y2 = m_Grid_Y;
						for (int l = 0; l <= grid_Y2; l++)
						{
							W_Data((byte)k, (byte)l, array[k, l]);
						}
					}
					ClearUndo();
					Busy--;
					if (Busy < 0)
					{
						Busy = 0;
					}
				}
				else
				{
					m_Grid_Y = value;
				}
			}
		}
	}

	public byte Grid_ShowLabels
	{
		get
		{
			return m_Grid_ShowLabels;
		}
		set
		{
			m_Grid_ShowLabels = value;
			if (m_Grid_ShowLabels == 0)
			{
				CopyLabelsToolStripMenuItem.Enabled = false;
				PasteLabelsToolStripMenuItem.Enabled = false;
				PasteLabelsInterpolateToolStripMenuItem.Enabled = false;
				CopyLabelsToolStripMenuItem.Enabled = false;
				ImportAxisMenuItem.Enabled = false;
			}
			else
			{
				CopyLabelsToolStripMenuItem.Enabled = true;
				PasteLabelsToolStripMenuItem.Enabled = true;
				PasteLabelsInterpolateToolStripMenuItem.Enabled = true;
				ImportAxisMenuItem.Enabled = true;
			}
			ReSize_Grid();
		}
	}

	public byte Grid_Transpose
	{
		get
		{
			return m_Grid_Transpose;
		}
		set
		{
			m_Grid_Transpose = value;
			ReSize_Grid();
		}
	}

	public byte Grid_TransposeCopyPaste
	{
		get
		{
			return m_Grid_TransposeCopyPaste;
		}
		set
		{
			m_Grid_TransposeCopyPaste = value;
		}
	}

	public byte Grid_GraphType
	{
		get
		{
			return m_Grid_GraphType;
		}
		set
		{
			m_Grid_GraphType = value;
			if (m_Grid_GraphType == 0)
			{
				GraphToolStripMenuItem.Enabled = false;
				((Control)Graph).Hide();
			}
			else
			{
				GraphToolStripMenuItem.Enabled = true;
			}
			m_Grid_ReDraw = 1;
		}
	}

	public byte Grid_ReDraw
	{
		get
		{
			return m_Grid_ReDraw;
		}
		set
		{
			m_Grid_ReDraw = value;
		}
	}

	public byte Grid_FreezeDraw
	{
		get
		{
			return m_Grid_FreezeDraw;
		}
		set
		{
			m_Grid_FreezeDraw = value;
		}
	}

	public float Grid_DataOffset
	{
		get
		{
			return m_Grid_DataOffset;
		}
		set
		{
			m_Grid_DataOffset = value;
			m_Grid_ReDraw = 1;
		}
	}

	public float Grid_DataScalar
	{
		get
		{
			return m_Grid_DataScalar;
		}
		set
		{
			m_Grid_DataScalar = value;
			if (m_Grid_DataScalar == 0f)
			{
				m_Grid_DataScalar = 1f;
			}
			m_Grid_ReDraw = 1;
		}
	}

	public int Grid_AxisStatus
	{
		get
		{
			return m_Grid_AxisStatus;
		}
		set
		{
			m_Grid_AxisStatus = value;
			if (m_Grid_AxisStatus == -1)
			{
				ImportAxisMenuItem.Enabled = false;
			}
			else
			{
				ImportAxisMenuItem.Enabled = true;
			}
		}
	}

	public int Grid_DataStatus
	{
		get
		{
			return m_Grid_DataStatus;
		}
		set
		{
			m_Grid_DataStatus = value;
		}
	}

	public byte Grid_DataSCopyPaste
	{
		get
		{
			return m_Grid_DataSCopyPaste;
		}
		set
		{
			m_Grid_DataSCopyPaste = value;
		}
	}

	public int Cell_W
	{
		get
		{
			return m_Cell_W;
		}
		set
		{
			m_Cell_W = value;
			ReSize_Grid();
		}
	}

	public int Cell_H
	{
		get
		{
			return m_Cell_H;
		}
		set
		{
			m_Cell_H = value;
			ReSize_Grid();
		}
	}

	public byte Cell_Auto_W
	{
		get
		{
			return m_Cell_Auto_W;
		}
		set
		{
			m_Cell_Auto_W = value;
			Check_Width();
			m_Grid_ReDraw = 1;
		}
	}

	public byte Cell_ShowChanges
	{
		get
		{
			return m_Cell_ShowChanges;
		}
		set
		{
			m_Cell_ShowChanges = value;
			m_Grid_ReDraw = 1;
		}
	}

	public byte Cell_CharMax
	{
		get
		{
			return m_Cell_CharMax;
		}
		set
		{
			m_Cell_CharMax = value;
			Check_Width();
			m_Grid_ReDraw = 1;
		}
	}

	public string Cell_Format
	{
		get
		{
			return m_Cell_Format;
		}
		set
		{
			m_Cell_Format = value;
			m_Grid_ReDraw = 1;
		}
	}

	public string Cell_LabelFormat
	{
		get
		{
			return m_Cell_LabelFormat;
		}
		set
		{
			m_Cell_LabelFormat = value;
			m_Grid_ReDraw = 1;
		}
	}

	public string Cell_CPFormat
	{
		get
		{
			return m_Cell_CPFormat;
		}
		set
		{
			m_Cell_CPFormat = value;
			m_Grid_ReDraw = 1;
		}
	}

	public Color Cell_LowCLR
	{
		get
		{
			return m_Cell_LowCLR;
		}
		set
		{
			m_Cell_LowCLR = value;
			m_Grid_ReDraw = 1;
		}
	}

	public Color Cell_HighCLR
	{
		get
		{
			return m_Cell_HighCLR;
		}
		set
		{
			m_Cell_HighCLR = value;
			m_Grid_ReDraw = 1;
		}
	}

	public Color Cell_FontCLR
	{
		get
		{
			return m_Cell_FontCLR;
		}
		set
		{
			m_Cell_FontCLR = value;
			m_Grid_ReDraw = 1;
		}
	}

	public Color Cell_LSelCLR
	{
		get
		{
			return m_Cell_LSelCLR;
		}
		set
		{
			m_Cell_LSelCLR = value;
			m_Grid_ReDraw = 1;
		}
	}

	public Color Cell_HSelCLR
	{
		get
		{
			return m_Cell_HSelCLR;
		}
		set
		{
			m_Cell_HSelCLR = value;
			m_Grid_ReDraw = 1;
		}
	}

	public Color Cell_FSelCLR
	{
		get
		{
			return m_Cell_FSelCLR;
		}
		set
		{
			m_Cell_FSelCLR = value;
			m_Grid_ReDraw = 1;
		}
	}

	public BCGridControl()
	{
		//IL_0048: Unknown result type (might be due to invalid IL or missing references)
		//IL_0052: Expected O, but got Unknown
		//IL_005b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0065: Expected O, but got Unknown
		//IL_006e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0078: Expected O, but got Unknown
		//IL_0081: Unknown result type (might be due to invalid IL or missing references)
		//IL_008b: Expected O, but got Unknown
		//IL_00a7: Unknown result type (might be due to invalid IL or missing references)
		//IL_00b1: Expected O, but got Unknown
		//IL_00ba: Unknown result type (might be due to invalid IL or missing references)
		//IL_00c4: Expected O, but got Unknown
		//IL_00ca: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d4: Expected O, but got Unknown
		//IL_00da: Unknown result type (might be due to invalid IL or missing references)
		//IL_00e4: Expected O, but got Unknown
		//IL_00ea: Unknown result type (might be due to invalid IL or missing references)
		//IL_00f4: Expected O, but got Unknown
		//IL_00fa: Unknown result type (might be due to invalid IL or missing references)
		//IL_0104: Expected O, but got Unknown
		//IL_010c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0116: Expected O, but got Unknown
		//IL_01a5: Unknown result type (might be due to invalid IL or missing references)
		//IL_01af: Expected O, but got Unknown
		//IL_01b0: Unknown result type (might be due to invalid IL or missing references)
		//IL_01ba: Expected O, but got Unknown
		//IL_01bb: Unknown result type (might be due to invalid IL or missing references)
		//IL_01c5: Expected O, but got Unknown
		//IL_01c6: Unknown result type (might be due to invalid IL or missing references)
		//IL_01d0: Expected O, but got Unknown
		//IL_01d1: Unknown result type (might be due to invalid IL or missing references)
		//IL_01db: Expected O, but got Unknown
		//IL_01dc: Unknown result type (might be due to invalid IL or missing references)
		//IL_01e6: Expected O, but got Unknown
		//IL_01e7: Unknown result type (might be due to invalid IL or missing references)
		//IL_01f1: Expected O, but got Unknown
		//IL_01f2: Unknown result type (might be due to invalid IL or missing references)
		//IL_01fc: Expected O, but got Unknown
		//IL_01fd: Unknown result type (might be due to invalid IL or missing references)
		//IL_0207: Expected O, but got Unknown
		//IL_0208: Unknown result type (might be due to invalid IL or missing references)
		//IL_0212: Expected O, but got Unknown
		//IL_0213: Unknown result type (might be due to invalid IL or missing references)
		//IL_021d: Expected O, but got Unknown
		//IL_021e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0228: Expected O, but got Unknown
		//IL_0229: Unknown result type (might be due to invalid IL or missing references)
		//IL_0233: Expected O, but got Unknown
		//IL_0234: Unknown result type (might be due to invalid IL or missing references)
		//IL_023e: Expected O, but got Unknown
		//IL_023f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0249: Expected O, but got Unknown
		//IL_024a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0254: Expected O, but got Unknown
		((UserControl)this).Load += BCGridControl_Load;
		((Control)this).Resize += BCGridControl_Resize;
		((Control)this).VisibleChanged += BCGridControl_VisibleChanged;
		((Control)this).KeyDown += new KeyEventHandler(Control_KeyDown);
		((Control)this).KeyUp += new KeyEventHandler(Control_KeyUp);
		((Control)this).KeyPress += new KeyPressEventHandler(Control_KeyPress);
		((Control)this).MouseMove += new MouseEventHandler(Control_MouseMove);
		((Control)this).MouseLeave += Contorl_MouseLeave;
		((Control)this).MouseDown += new MouseEventHandler(Contorl_MouseDown);
		((Control)this).MouseUp += new MouseEventHandler(Control_MouseUp);
		T_Brush = new SolidBrush(Color.Black);
		T_Pen = new Pen(Color.Black);
		C_Brush = new SolidBrush(Color.Black);
		C_Pen = new Pen(Color.Black);
		IsDrawling = 1;
		Graph = new Form();
		IsDrawlingG = 1;
		XD = -0.5f;
		YD = 3.14f;
		ZD = 0f;
		XDS = -0.5f;
		YDS = 3.14f;
		ZDS = 0f;
		VW_X = 0f;
		VW_Y = -150f;
		VW_Z = -1500f;
		VW_ZM = 1f;
		GMSX = 1;
		GMSY = 1;
		GMSS = 1f;
		Toolbar = new Form();
		TB_Text1 = new TextBox();
		TB_Btn1 = new Button();
		TB_Btn2 = new Button();
		TB_Btn3 = new Button();
		TB_Btn4 = new Button();
		TB_Btn5 = new Button();
		TB_Btn6 = new Button();
		TB_Btn7 = new Button();
		TB_Btn8 = new Button();
		TB_Btn9 = new Button();
		TB_Btn10 = new Button();
		TB_Btn11 = new Button();
		TB_Btn12 = new Button();
		TB_Btn13 = new Button();
		TB_Timer1 = new Timer();
		Mouse_Over = 0;
		Mouse_OverP = 0;
		DFocus = 0;
		DFocusP = 0;
		MAX_X = 128;
		MAX_Y = 128;
		MAX_U = 16;
		Busy = 0;
		UndoC = 0;
		Init = 0;
		m_Grid_VisibleName = "";
		m_Grid_X = 4;
		m_Grid_Y = 4;
		m_Grid_ShowLabels = 0;
		m_Grid_Transpose = 0;
		m_Grid_TransposeCopyPaste = 0;
		m_Grid_GraphType = 1;
		m_Grid_ReDraw = 0;
		m_Grid_FreezeDraw = 0;
		m_Grid_AxisStatus = 0;
		m_Grid_DataStatus = 0;
		m_Grid_DataOffset = 0f;
		m_Grid_DataScalar = 1f;
		m_Grid_DataSCopyPaste = 1;
		m_Cell_W = 32;
		m_Cell_H = 12;
		m_Cell_Auto_W = 0;
		m_Cell_ShowChanges = 0;
		m_Cell_CharMax = 5;
		m_Cell_Format = "##0.0";
		m_Cell_LabelFormat = "####0";
		m_Cell_CPFormat = "###,###,###,##0.############";
		m_Cell_LowCLR = Color.White;
		m_Cell_HighCLR = Color.RoyalBlue;
		m_Cell_FontCLR = Color.Black;
		m_Cell_LSelCLR = Color.Red;
		m_Cell_HSelCLR = Color.DarkRed;
		m_Cell_FSelCLR = Color.White;
		MultiSelect = -1;
		LX = 1;
		LY = 1;
		L2X = -1;
		L2Y = -1;
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
			((ContainerControl)this).Dispose(disposing);
		}
	}

	[DebuggerStepThrough]
	private void InitializeComponent()
	{
		//IL_000c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0016: Expected O, but got Unknown
		//IL_001d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0027: Expected O, but got Unknown
		//IL_002e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0038: Expected O, but got Unknown
		//IL_0039: Unknown result type (might be due to invalid IL or missing references)
		//IL_0043: Expected O, but got Unknown
		//IL_0044: Unknown result type (might be due to invalid IL or missing references)
		//IL_004e: Expected O, but got Unknown
		//IL_004f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0059: Expected O, but got Unknown
		//IL_005a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0064: Expected O, but got Unknown
		//IL_0065: Unknown result type (might be due to invalid IL or missing references)
		//IL_006f: Expected O, but got Unknown
		//IL_0070: Unknown result type (might be due to invalid IL or missing references)
		//IL_007a: Expected O, but got Unknown
		//IL_007b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0085: Expected O, but got Unknown
		//IL_0086: Unknown result type (might be due to invalid IL or missing references)
		//IL_0090: Expected O, but got Unknown
		//IL_0091: Unknown result type (might be due to invalid IL or missing references)
		//IL_009b: Expected O, but got Unknown
		//IL_009c: Unknown result type (might be due to invalid IL or missing references)
		//IL_00a6: Expected O, but got Unknown
		//IL_00a7: Unknown result type (might be due to invalid IL or missing references)
		//IL_00b1: Expected O, but got Unknown
		//IL_00b2: Unknown result type (might be due to invalid IL or missing references)
		//IL_00bc: Expected O, but got Unknown
		//IL_00bd: Unknown result type (might be due to invalid IL or missing references)
		//IL_00c7: Expected O, but got Unknown
		//IL_00c8: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d2: Expected O, but got Unknown
		//IL_00d3: Unknown result type (might be due to invalid IL or missing references)
		//IL_00dd: Expected O, but got Unknown
		//IL_00de: Unknown result type (might be due to invalid IL or missing references)
		//IL_00e8: Expected O, but got Unknown
		//IL_00e9: Unknown result type (might be due to invalid IL or missing references)
		//IL_00f3: Expected O, but got Unknown
		//IL_00f4: Unknown result type (might be due to invalid IL or missing references)
		//IL_00fe: Expected O, but got Unknown
		//IL_00ff: Unknown result type (might be due to invalid IL or missing references)
		//IL_0109: Expected O, but got Unknown
		//IL_010a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0114: Expected O, but got Unknown
		//IL_0115: Unknown result type (might be due to invalid IL or missing references)
		//IL_011f: Expected O, but got Unknown
		//IL_0120: Unknown result type (might be due to invalid IL or missing references)
		//IL_012a: Expected O, but got Unknown
		//IL_012b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0135: Expected O, but got Unknown
		//IL_0136: Unknown result type (might be due to invalid IL or missing references)
		//IL_0140: Expected O, but got Unknown
		//IL_0141: Unknown result type (might be due to invalid IL or missing references)
		//IL_014b: Expected O, but got Unknown
		//IL_014c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0156: Expected O, but got Unknown
		//IL_0157: Unknown result type (might be due to invalid IL or missing references)
		//IL_0161: Expected O, but got Unknown
		//IL_0162: Unknown result type (might be due to invalid IL or missing references)
		//IL_016c: Expected O, but got Unknown
		//IL_016d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0177: Expected O, but got Unknown
		//IL_0178: Unknown result type (might be due to invalid IL or missing references)
		//IL_0182: Expected O, but got Unknown
		//IL_0183: Unknown result type (might be due to invalid IL or missing references)
		//IL_018d: Expected O, but got Unknown
		//IL_018e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0198: Expected O, but got Unknown
		//IL_0199: Unknown result type (might be due to invalid IL or missing references)
		//IL_01a3: Expected O, but got Unknown
		//IL_01a4: Unknown result type (might be due to invalid IL or missing references)
		//IL_01ae: Expected O, but got Unknown
		//IL_01af: Unknown result type (might be due to invalid IL or missing references)
		//IL_01b9: Expected O, but got Unknown
		//IL_01ba: Unknown result type (might be due to invalid IL or missing references)
		//IL_01c4: Expected O, but got Unknown
		//IL_01c5: Unknown result type (might be due to invalid IL or missing references)
		//IL_01cf: Expected O, but got Unknown
		//IL_01d0: Unknown result type (might be due to invalid IL or missing references)
		//IL_01da: Expected O, but got Unknown
		//IL_01db: Unknown result type (might be due to invalid IL or missing references)
		//IL_01e5: Expected O, but got Unknown
		//IL_01e6: Unknown result type (might be due to invalid IL or missing references)
		//IL_01f0: Expected O, but got Unknown
		//IL_01f1: Unknown result type (might be due to invalid IL or missing references)
		//IL_01fb: Expected O, but got Unknown
		//IL_01fc: Unknown result type (might be due to invalid IL or missing references)
		//IL_0206: Expected O, but got Unknown
		//IL_0207: Unknown result type (might be due to invalid IL or missing references)
		//IL_0211: Expected O, but got Unknown
		//IL_0212: Unknown result type (might be due to invalid IL or missing references)
		//IL_021c: Expected O, but got Unknown
		//IL_021d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0227: Expected O, but got Unknown
		//IL_0228: Unknown result type (might be due to invalid IL or missing references)
		//IL_0232: Expected O, but got Unknown
		//IL_0233: Unknown result type (might be due to invalid IL or missing references)
		//IL_023d: Expected O, but got Unknown
		//IL_023e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0248: Expected O, but got Unknown
		//IL_0249: Unknown result type (might be due to invalid IL or missing references)
		//IL_0253: Expected O, but got Unknown
		//IL_0254: Unknown result type (might be due to invalid IL or missing references)
		//IL_025e: Expected O, but got Unknown
		//IL_025f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0269: Expected O, but got Unknown
		//IL_026a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0274: Expected O, but got Unknown
		//IL_0275: Unknown result type (might be due to invalid IL or missing references)
		//IL_027f: Expected O, but got Unknown
		//IL_0280: Unknown result type (might be due to invalid IL or missing references)
		//IL_028a: Expected O, but got Unknown
		//IL_028b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0295: Expected O, but got Unknown
		//IL_0296: Unknown result type (might be due to invalid IL or missing references)
		//IL_02a0: Expected O, but got Unknown
		//IL_02a1: Unknown result type (might be due to invalid IL or missing references)
		//IL_02ab: Expected O, but got Unknown
		//IL_02ac: Unknown result type (might be due to invalid IL or missing references)
		//IL_02b6: Expected O, but got Unknown
		//IL_02b7: Unknown result type (might be due to invalid IL or missing references)
		//IL_02c1: Expected O, but got Unknown
		//IL_02c2: Unknown result type (might be due to invalid IL or missing references)
		//IL_02cc: Expected O, but got Unknown
		//IL_02cd: Unknown result type (might be due to invalid IL or missing references)
		//IL_02d7: Expected O, but got Unknown
		//IL_02d8: Unknown result type (might be due to invalid IL or missing references)
		//IL_02e2: Expected O, but got Unknown
		//IL_02e3: Unknown result type (might be due to invalid IL or missing references)
		//IL_02ed: Expected O, but got Unknown
		//IL_02ee: Unknown result type (might be due to invalid IL or missing references)
		//IL_02f8: Expected O, but got Unknown
		//IL_02f9: Unknown result type (might be due to invalid IL or missing references)
		//IL_0303: Expected O, but got Unknown
		//IL_0304: Unknown result type (might be due to invalid IL or missing references)
		//IL_030e: Expected O, but got Unknown
		//IL_030f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0319: Expected O, but got Unknown
		components = new Container();
		TextBox1 = new TextBox();
		Timer1 = new Timer(components);
		DataMenuStrip = new ContextMenuStrip(components);
		CopyToolStripMenuItem = new ToolStripMenuItem();
		CopyLabelsToolStripMenuItem = new ToolStripMenuItem();
		PasteToolStripMenuItem = new ToolStripMenuItem();
		PasteLabelsToolStripMenuItem = new ToolStripMenuItem();
		PasteLabelsInterpolateToolStripMenuItem = new ToolStripMenuItem();
		ToolStripSeparator7 = new ToolStripSeparator();
		PasteAddToolStripMenuItem = new ToolStripMenuItem();
		PasteSubtractToolStripMenuItem = new ToolStripMenuItem();
		ToolStripSeparator8 = new ToolStripSeparator();
		PasteMultiplyToolStripMenuItem = new ToolStripMenuItem();
		PasteMultiplyPctToolStripMenuItem = new ToolStripMenuItem();
		PasteMultiplyPctHalfToolStripMenuItem = new ToolStripMenuItem();
		PasteDivideToolStripMenuItem = new ToolStripMenuItem();
		ToolStripSeparator9 = new ToolStripSeparator();
		PasteAverageToolStripMenuItem = new ToolStripMenuItem();
		ToolStripSeparator14 = new ToolStripSeparator();
		EditToolStripMenuItem = new ToolStripMenuItem();
		ToolStripTextBox1 = new ToolStripTextBox();
		FillToolStripMenuItem = new ToolStripMenuItem();
		ToolStripSeparator3 = new ToolStripSeparator();
		AddToolStripMenuItem = new ToolStripMenuItem();
		SubtractToolStripMenuItem = new ToolStripMenuItem();
		ToolStripSeparator4 = new ToolStripSeparator();
		MultiplyToolStripMenuItem = new ToolStripMenuItem();
		DivideToolStripMenuItem = new ToolStripMenuItem();
		ToolStripSeparator10 = new ToolStripSeparator();
		ManipulateToolStripMenuItem = new ToolStripMenuItem();
		SmoothToolStripMenuItem = new ToolStripMenuItem();
		SmoothHorizontalToolStripMenuItem = new ToolStripMenuItem();
		SmoothVerticalToolStripMenuItem = new ToolStripMenuItem();
		ToolStripSeparator5 = new ToolStripSeparator();
		InterpolateToolStripMenuItem = new ToolStripMenuItem();
		InterpolateHorizontalToolStripMenuItem = new ToolStripMenuItem();
		InterpolateVerticalToolStripMenuItem = new ToolStripMenuItem();
		ToolStripSeparator6 = new ToolStripSeparator();
		ExtrapolateToolStripMenuItem = new ToolStripMenuItem();
		SelectToolStripMenuItem = new ToolStripMenuItem();
		SelectNullsToolStripMenuItem = new ToolStripMenuItem();
		SelectNonNullsToolStripMenuItem = new ToolStripMenuItem();
		SelectZerosToolStripMenuItem = new ToolStripMenuItem();
		SelectNonZerosToolStripMenuItem = new ToolStripMenuItem();
		SelectPositiveToolStripMenuItem = new ToolStripMenuItem();
		SelectNegativeToolStripMenuItem = new ToolStripMenuItem();
		OtherMenuItem = new ToolStripMenuItem();
		TransposeClipboardToolStripMenuItem = new ToolStripMenuItem();
		ToolStripSeparator15 = new ToolStripSeparator();
		ToolStripTextBox2 = new ToolStripTextBox();
		ScaleXAxisMenuItem = new ToolStripMenuItem();
		ScaleYAxisMenuItem = new ToolStripMenuItem();
		ToolStripSeparator16 = new ToolStripSeparator();
		ImportAxisMenuItem = new ToolStripMenuItem();
		ToolStripSeparator11 = new ToolStripSeparator();
		ClearChangedFlagToolStripMenuItem = new ToolStripMenuItem();
		ToggleChangeFlagDisplayToolStripMenuItem = new ToolStripMenuItem();
		ToolStripSeparator12 = new ToolStripSeparator();
		ClearTableToZerosToolStripMenuItem = new ToolStripMenuItem();
		ClearTableToNullsToolStripMenuItem = new ToolStripMenuItem();
		ToolStripSeparator13 = new ToolStripSeparator();
		ConvertZerosToNullsToolStripMenuItem = new ToolStripMenuItem();
		ConvertNullsToZerosToolStripMenuItem = new ToolStripMenuItem();
		ToolStripSeparator2 = new ToolStripSeparator();
		GraphToolStripMenuItem = new ToolStripMenuItem();
		Graph2DToolStripMenuItem = new ToolStripMenuItem();
		Graph3DToolStripMenuItem = new ToolStripMenuItem();
		ToolbarToolStripMenuItem = new ToolStripMenuItem();
		ToolStripSeparator1 = new ToolStripSeparator();
		UndoToolStripMenuItem = new ToolStripMenuItem();
		((Control)DataMenuStrip).SuspendLayout();
		((Control)this).SuspendLayout();
		((TextBoxBase)TextBox1).BorderStyle = (BorderStyle)1;
		TextBox textBox = TextBox1;
		Point location = new Point(3, 3);
		((Control)textBox).Location = location;
		((Control)TextBox1).Name = "TextBox1";
		TextBox textBox2 = TextBox1;
		Size size = new Size(62, 20);
		((Control)textBox2).Size = size;
		((Control)TextBox1).TabIndex = 0;
		((Control)TextBox1).Visible = false;
		Timer1.Enabled = true;
		((ToolStrip)DataMenuStrip).Items.AddRange((ToolStripItem[])(object)new ToolStripItem[13]
		{
			(ToolStripItem)CopyToolStripMenuItem,
			(ToolStripItem)PasteToolStripMenuItem,
			(ToolStripItem)ToolStripSeparator14,
			(ToolStripItem)EditToolStripMenuItem,
			(ToolStripItem)ToolStripSeparator10,
			(ToolStripItem)ManipulateToolStripMenuItem,
			(ToolStripItem)SelectToolStripMenuItem,
			(ToolStripItem)OtherMenuItem,
			(ToolStripItem)ToolStripSeparator2,
			(ToolStripItem)GraphToolStripMenuItem,
			(ToolStripItem)ToolbarToolStripMenuItem,
			(ToolStripItem)ToolStripSeparator1,
			(ToolStripItem)UndoToolStripMenuItem
		});
		((Control)DataMenuStrip).Name = "DatatMenuStrip";
		ContextMenuStrip dataMenuStrip = DataMenuStrip;
		size = new Size(153, 248);
		((Control)dataMenuStrip).Size = size;
		((ToolStripDropDownItem)CopyToolStripMenuItem).DropDownItems.AddRange((ToolStripItem[])(object)new ToolStripItem[1] { (ToolStripItem)CopyLabelsToolStripMenuItem });
		((ToolStripItem)CopyToolStripMenuItem).Name = "CopyToolStripMenuItem";
		ToolStripMenuItem copyToolStripMenuItem = CopyToolStripMenuItem;
		size = new Size(152, 22);
		((ToolStripItem)copyToolStripMenuItem).Size = size;
		((ToolStripItem)CopyToolStripMenuItem).Text = "Copy";
		((ToolStripItem)CopyLabelsToolStripMenuItem).Name = "CopyLabelsToolStripMenuItem";
		ToolStripMenuItem copyLabelsToolStripMenuItem = CopyLabelsToolStripMenuItem;
		size = new Size(164, 22);
		((ToolStripItem)copyLabelsToolStripMenuItem).Size = size;
		((ToolStripItem)CopyLabelsToolStripMenuItem).Text = "Copy with Labels";
		((ToolStripDropDownItem)PasteToolStripMenuItem).DropDownItems.AddRange((ToolStripItem[])(object)new ToolStripItem[12]
		{
			(ToolStripItem)PasteLabelsToolStripMenuItem,
			(ToolStripItem)PasteLabelsInterpolateToolStripMenuItem,
			(ToolStripItem)ToolStripSeparator7,
			(ToolStripItem)PasteAddToolStripMenuItem,
			(ToolStripItem)PasteSubtractToolStripMenuItem,
			(ToolStripItem)ToolStripSeparator8,
			(ToolStripItem)PasteMultiplyToolStripMenuItem,
			(ToolStripItem)PasteMultiplyPctToolStripMenuItem,
			(ToolStripItem)PasteMultiplyPctHalfToolStripMenuItem,
			(ToolStripItem)PasteDivideToolStripMenuItem,
			(ToolStripItem)ToolStripSeparator9,
			(ToolStripItem)PasteAverageToolStripMenuItem
		});
		((ToolStripItem)PasteToolStripMenuItem).Name = "PasteToolStripMenuItem";
		ToolStripMenuItem pasteToolStripMenuItem = PasteToolStripMenuItem;
		size = new Size(152, 22);
		((ToolStripItem)pasteToolStripMenuItem).Size = size;
		((ToolStripItem)PasteToolStripMenuItem).Text = "Paste";
		((ToolStripItem)PasteLabelsToolStripMenuItem).Name = "PasteLabelsToolStripMenuItem";
		ToolStripMenuItem pasteLabelsToolStripMenuItem = PasteLabelsToolStripMenuItem;
		size = new Size(224, 22);
		((ToolStripItem)pasteLabelsToolStripMenuItem).Size = size;
		((ToolStripItem)PasteLabelsToolStripMenuItem).Text = "Paste with Labels";
		((ToolStripItem)PasteLabelsInterpolateToolStripMenuItem).Name = "PasteLabelsInterpolateToolStripMenuItem";
		ToolStripMenuItem pasteLabelsInterpolateToolStripMenuItem = PasteLabelsInterpolateToolStripMenuItem;
		size = new Size(224, 22);
		((ToolStripItem)pasteLabelsInterpolateToolStripMenuItem).Size = size;
		((ToolStripItem)PasteLabelsInterpolateToolStripMenuItem).Text = "Paste with Labels Interpolate";
		((ToolStripItem)ToolStripSeparator7).Name = "ToolStripSeparator7";
		ToolStripSeparator toolStripSeparator = ToolStripSeparator7;
		size = new Size(221, 6);
		((ToolStripItem)toolStripSeparator).Size = size;
		((ToolStripItem)PasteAddToolStripMenuItem).Name = "PasteAddToolStripMenuItem";
		ToolStripMenuItem pasteAddToolStripMenuItem = PasteAddToolStripMenuItem;
		size = new Size(224, 22);
		((ToolStripItem)pasteAddToolStripMenuItem).Size = size;
		((ToolStripItem)PasteAddToolStripMenuItem).Text = "Paste Add";
		((ToolStripItem)PasteSubtractToolStripMenuItem).Name = "PasteSubtractToolStripMenuItem";
		ToolStripMenuItem pasteSubtractToolStripMenuItem = PasteSubtractToolStripMenuItem;
		size = new Size(224, 22);
		((ToolStripItem)pasteSubtractToolStripMenuItem).Size = size;
		((ToolStripItem)PasteSubtractToolStripMenuItem).Text = "Paste Subtract";
		((ToolStripItem)ToolStripSeparator8).Name = "ToolStripSeparator8";
		ToolStripSeparator toolStripSeparator2 = ToolStripSeparator8;
		size = new Size(221, 6);
		((ToolStripItem)toolStripSeparator2).Size = size;
		((ToolStripItem)PasteMultiplyToolStripMenuItem).Name = "PasteMultiplyToolStripMenuItem";
		ToolStripMenuItem pasteMultiplyToolStripMenuItem = PasteMultiplyToolStripMenuItem;
		size = new Size(224, 22);
		((ToolStripItem)pasteMultiplyToolStripMenuItem).Size = size;
		((ToolStripItem)PasteMultiplyToolStripMenuItem).Text = "Paste Multiply";
		((ToolStripItem)PasteMultiplyPctToolStripMenuItem).Name = "PasteMultiplyPctToolStripMenuItem";
		ToolStripMenuItem pasteMultiplyPctToolStripMenuItem = PasteMultiplyPctToolStripMenuItem;
		size = new Size(224, 22);
		((ToolStripItem)pasteMultiplyPctToolStripMenuItem).Size = size;
		((ToolStripItem)PasteMultiplyPctToolStripMenuItem).Text = "Paste Multiply %";
		((ToolStripItem)PasteMultiplyPctHalfToolStripMenuItem).Name = "PasteMultiplyPctHalfToolStripMenuItem";
		ToolStripMenuItem pasteMultiplyPctHalfToolStripMenuItem = PasteMultiplyPctHalfToolStripMenuItem;
		size = new Size(224, 22);
		((ToolStripItem)pasteMultiplyPctHalfToolStripMenuItem).Size = size;
		((ToolStripItem)PasteMultiplyPctHalfToolStripMenuItem).Text = "Paste Multiply % Half";
		((ToolStripItem)PasteDivideToolStripMenuItem).Name = "PasteDivideToolStripMenuItem";
		ToolStripMenuItem pasteDivideToolStripMenuItem = PasteDivideToolStripMenuItem;
		size = new Size(224, 22);
		((ToolStripItem)pasteDivideToolStripMenuItem).Size = size;
		((ToolStripItem)PasteDivideToolStripMenuItem).Text = "Paste Divide";
		((ToolStripItem)ToolStripSeparator9).Name = "ToolStripSeparator9";
		ToolStripSeparator toolStripSeparator3 = ToolStripSeparator9;
		size = new Size(221, 6);
		((ToolStripItem)toolStripSeparator3).Size = size;
		((ToolStripItem)PasteAverageToolStripMenuItem).Name = "PasteAverageToolStripMenuItem";
		ToolStripMenuItem pasteAverageToolStripMenuItem = PasteAverageToolStripMenuItem;
		size = new Size(224, 22);
		((ToolStripItem)pasteAverageToolStripMenuItem).Size = size;
		((ToolStripItem)PasteAverageToolStripMenuItem).Text = "Paste Average";
		((ToolStripItem)ToolStripSeparator14).Name = "ToolStripSeparator14";
		ToolStripSeparator toolStripSeparator4 = ToolStripSeparator14;
		size = new Size(149, 6);
		((ToolStripItem)toolStripSeparator4).Size = size;
		((ToolStripDropDownItem)EditToolStripMenuItem).DropDownItems.AddRange((ToolStripItem[])(object)new ToolStripItem[8]
		{
			(ToolStripItem)ToolStripTextBox1,
			(ToolStripItem)FillToolStripMenuItem,
			(ToolStripItem)ToolStripSeparator3,
			(ToolStripItem)AddToolStripMenuItem,
			(ToolStripItem)SubtractToolStripMenuItem,
			(ToolStripItem)ToolStripSeparator4,
			(ToolStripItem)MultiplyToolStripMenuItem,
			(ToolStripItem)DivideToolStripMenuItem
		});
		((ToolStripItem)EditToolStripMenuItem).Name = "EditToolStripMenuItem";
		ToolStripMenuItem editToolStripMenuItem = EditToolStripMenuItem;
		size = new Size(152, 22);
		((ToolStripItem)editToolStripMenuItem).Size = size;
		((ToolStripItem)EditToolStripMenuItem).Text = "Edit";
		ToolStripTextBox1.BorderStyle = (BorderStyle)1;
		((ToolStripItem)ToolStripTextBox1).Name = "ToolStripTextBox1";
		ToolStripTextBox toolStripTextBox = ToolStripTextBox1;
		size = new Size(100, 23);
		((ToolStripControlHost)toolStripTextBox).Size = size;
		((ToolStripItem)FillToolStripMenuItem).Name = "FillToolStripMenuItem";
		ToolStripMenuItem fillToolStripMenuItem = FillToolStripMenuItem;
		size = new Size(160, 22);
		((ToolStripItem)fillToolStripMenuItem).Size = size;
		((ToolStripItem)FillToolStripMenuItem).Text = "Fill";
		((ToolStripItem)ToolStripSeparator3).Name = "ToolStripSeparator3";
		ToolStripSeparator toolStripSeparator5 = ToolStripSeparator3;
		size = new Size(157, 6);
		((ToolStripItem)toolStripSeparator5).Size = size;
		((ToolStripItem)AddToolStripMenuItem).Name = "AddToolStripMenuItem";
		ToolStripMenuItem addToolStripMenuItem = AddToolStripMenuItem;
		size = new Size(160, 22);
		((ToolStripItem)addToolStripMenuItem).Size = size;
		((ToolStripItem)AddToolStripMenuItem).Text = "Add";
		((ToolStripItem)SubtractToolStripMenuItem).Name = "SubtractToolStripMenuItem";
		ToolStripMenuItem subtractToolStripMenuItem = SubtractToolStripMenuItem;
		size = new Size(160, 22);
		((ToolStripItem)subtractToolStripMenuItem).Size = size;
		((ToolStripItem)SubtractToolStripMenuItem).Text = "Subtract";
		((ToolStripItem)ToolStripSeparator4).Name = "ToolStripSeparator4";
		ToolStripSeparator toolStripSeparator6 = ToolStripSeparator4;
		size = new Size(157, 6);
		((ToolStripItem)toolStripSeparator6).Size = size;
		((ToolStripItem)MultiplyToolStripMenuItem).Name = "MultiplyToolStripMenuItem";
		ToolStripMenuItem multiplyToolStripMenuItem = MultiplyToolStripMenuItem;
		size = new Size(160, 22);
		((ToolStripItem)multiplyToolStripMenuItem).Size = size;
		((ToolStripItem)MultiplyToolStripMenuItem).Text = "Multiply";
		((ToolStripItem)DivideToolStripMenuItem).Name = "DivideToolStripMenuItem";
		ToolStripMenuItem divideToolStripMenuItem = DivideToolStripMenuItem;
		size = new Size(160, 22);
		((ToolStripItem)divideToolStripMenuItem).Size = size;
		((ToolStripItem)DivideToolStripMenuItem).Text = "Divide";
		((ToolStripItem)ToolStripSeparator10).Name = "ToolStripSeparator10";
		ToolStripSeparator toolStripSeparator7 = ToolStripSeparator10;
		size = new Size(149, 6);
		((ToolStripItem)toolStripSeparator7).Size = size;
		((ToolStripDropDownItem)ManipulateToolStripMenuItem).DropDownItems.AddRange((ToolStripItem[])(object)new ToolStripItem[9]
		{
			(ToolStripItem)SmoothToolStripMenuItem,
			(ToolStripItem)SmoothHorizontalToolStripMenuItem,
			(ToolStripItem)SmoothVerticalToolStripMenuItem,
			(ToolStripItem)ToolStripSeparator5,
			(ToolStripItem)InterpolateToolStripMenuItem,
			(ToolStripItem)InterpolateHorizontalToolStripMenuItem,
			(ToolStripItem)InterpolateVerticalToolStripMenuItem,
			(ToolStripItem)ToolStripSeparator6,
			(ToolStripItem)ExtrapolateToolStripMenuItem
		});
		((ToolStripItem)ManipulateToolStripMenuItem).Name = "ManipulateToolStripMenuItem";
		ToolStripMenuItem manipulateToolStripMenuItem = ManipulateToolStripMenuItem;
		size = new Size(152, 22);
		((ToolStripItem)manipulateToolStripMenuItem).Size = size;
		((ToolStripItem)ManipulateToolStripMenuItem).Text = "Manipulate";
		((ToolStripItem)SmoothToolStripMenuItem).Name = "SmoothToolStripMenuItem";
		ToolStripMenuItem smoothToolStripMenuItem = SmoothToolStripMenuItem;
		size = new Size(189, 22);
		((ToolStripItem)smoothToolStripMenuItem).Size = size;
		((ToolStripItem)SmoothToolStripMenuItem).Text = "Smooth";
		((ToolStripItem)SmoothHorizontalToolStripMenuItem).Name = "SmoothHorizontalToolStripMenuItem";
		ToolStripMenuItem smoothHorizontalToolStripMenuItem = SmoothHorizontalToolStripMenuItem;
		size = new Size(189, 22);
		((ToolStripItem)smoothHorizontalToolStripMenuItem).Size = size;
		((ToolStripItem)SmoothHorizontalToolStripMenuItem).Text = "Smooth Horizontal";
		((ToolStripItem)SmoothVerticalToolStripMenuItem).Name = "SmoothVerticalToolStripMenuItem";
		ToolStripMenuItem smoothVerticalToolStripMenuItem = SmoothVerticalToolStripMenuItem;
		size = new Size(189, 22);
		((ToolStripItem)smoothVerticalToolStripMenuItem).Size = size;
		((ToolStripItem)SmoothVerticalToolStripMenuItem).Text = "Smooth Vertical";
		((ToolStripItem)ToolStripSeparator5).Name = "ToolStripSeparator5";
		ToolStripSeparator toolStripSeparator8 = ToolStripSeparator5;
		size = new Size(186, 6);
		((ToolStripItem)toolStripSeparator8).Size = size;
		((ToolStripItem)InterpolateToolStripMenuItem).Name = "InterpolateToolStripMenuItem";
		ToolStripMenuItem interpolateToolStripMenuItem = InterpolateToolStripMenuItem;
		size = new Size(189, 22);
		((ToolStripItem)interpolateToolStripMenuItem).Size = size;
		((ToolStripItem)InterpolateToolStripMenuItem).Text = "Interpolate";
		((ToolStripItem)InterpolateHorizontalToolStripMenuItem).Name = "InterpolateHorizontalToolStripMenuItem";
		ToolStripMenuItem interpolateHorizontalToolStripMenuItem = InterpolateHorizontalToolStripMenuItem;
		size = new Size(189, 22);
		((ToolStripItem)interpolateHorizontalToolStripMenuItem).Size = size;
		((ToolStripItem)InterpolateHorizontalToolStripMenuItem).Text = "Interpolate Horizontal";
		((ToolStripItem)InterpolateVerticalToolStripMenuItem).Name = "InterpolateVerticalToolStripMenuItem";
		ToolStripMenuItem interpolateVerticalToolStripMenuItem = InterpolateVerticalToolStripMenuItem;
		size = new Size(189, 22);
		((ToolStripItem)interpolateVerticalToolStripMenuItem).Size = size;
		((ToolStripItem)InterpolateVerticalToolStripMenuItem).Text = "Interpolate Vertical";
		((ToolStripItem)ToolStripSeparator6).Name = "ToolStripSeparator6";
		ToolStripSeparator toolStripSeparator9 = ToolStripSeparator6;
		size = new Size(186, 6);
		((ToolStripItem)toolStripSeparator9).Size = size;
		((ToolStripItem)ExtrapolateToolStripMenuItem).Name = "ExtrapolateToolStripMenuItem";
		ToolStripMenuItem extrapolateToolStripMenuItem = ExtrapolateToolStripMenuItem;
		size = new Size(189, 22);
		((ToolStripItem)extrapolateToolStripMenuItem).Size = size;
		((ToolStripItem)ExtrapolateToolStripMenuItem).Text = "Extrapolate";
		((ToolStripDropDownItem)SelectToolStripMenuItem).DropDownItems.AddRange((ToolStripItem[])(object)new ToolStripItem[6]
		{
			(ToolStripItem)SelectNullsToolStripMenuItem,
			(ToolStripItem)SelectNonNullsToolStripMenuItem,
			(ToolStripItem)SelectZerosToolStripMenuItem,
			(ToolStripItem)SelectNonZerosToolStripMenuItem,
			(ToolStripItem)SelectPositiveToolStripMenuItem,
			(ToolStripItem)SelectNegativeToolStripMenuItem
		});
		((ToolStripItem)SelectToolStripMenuItem).Name = "SelectToolStripMenuItem";
		ToolStripMenuItem selectToolStripMenuItem = SelectToolStripMenuItem;
		size = new Size(152, 22);
		((ToolStripItem)selectToolStripMenuItem).Size = size;
		((ToolStripItem)SelectToolStripMenuItem).Text = "Select";
		((ToolStripItem)SelectNullsToolStripMenuItem).Name = "SelectNullsToolStripMenuItem";
		ToolStripMenuItem selectNullsToolStripMenuItem = SelectNullsToolStripMenuItem;
		size = new Size(168, 22);
		((ToolStripItem)selectNullsToolStripMenuItem).Size = size;
		((ToolStripItem)SelectNullsToolStripMenuItem).Text = "Select Null's";
		((ToolStripItem)SelectNonNullsToolStripMenuItem).Name = "SelectNonNullsToolStripMenuItem";
		ToolStripMenuItem selectNonNullsToolStripMenuItem = SelectNonNullsToolStripMenuItem;
		size = new Size(168, 22);
		((ToolStripItem)selectNonNullsToolStripMenuItem).Size = size;
		((ToolStripItem)SelectNonNullsToolStripMenuItem).Text = "Select Non-Null's";
		((ToolStripItem)SelectZerosToolStripMenuItem).Name = "SelectZerosToolStripMenuItem";
		ToolStripMenuItem selectZerosToolStripMenuItem = SelectZerosToolStripMenuItem;
		size = new Size(168, 22);
		((ToolStripItem)selectZerosToolStripMenuItem).Size = size;
		((ToolStripItem)SelectZerosToolStripMenuItem).Text = "Select Zero's";
		((ToolStripItem)SelectNonZerosToolStripMenuItem).Name = "SelectNonZerosToolStripMenuItem";
		ToolStripMenuItem selectNonZerosToolStripMenuItem = SelectNonZerosToolStripMenuItem;
		size = new Size(168, 22);
		((ToolStripItem)selectNonZerosToolStripMenuItem).Size = size;
		((ToolStripItem)SelectNonZerosToolStripMenuItem).Text = "Select Non-Zero's";
		((ToolStripItem)SelectPositiveToolStripMenuItem).Name = "SelectPositiveToolStripMenuItem";
		ToolStripMenuItem selectPositiveToolStripMenuItem = SelectPositiveToolStripMenuItem;
		size = new Size(168, 22);
		((ToolStripItem)selectPositiveToolStripMenuItem).Size = size;
		((ToolStripItem)SelectPositiveToolStripMenuItem).Text = "Select Positive";
		((ToolStripItem)SelectNegativeToolStripMenuItem).Name = "SelectNegativeToolStripMenuItem";
		ToolStripMenuItem selectNegativeToolStripMenuItem = SelectNegativeToolStripMenuItem;
		size = new Size(168, 22);
		((ToolStripItem)selectNegativeToolStripMenuItem).Size = size;
		((ToolStripItem)SelectNegativeToolStripMenuItem).Text = "Select Negative";
		((ToolStripDropDownItem)OtherMenuItem).DropDownItems.AddRange((ToolStripItem[])(object)new ToolStripItem[16]
		{
			(ToolStripItem)TransposeClipboardToolStripMenuItem,
			(ToolStripItem)ToolStripSeparator15,
			(ToolStripItem)ToolStripTextBox2,
			(ToolStripItem)ScaleXAxisMenuItem,
			(ToolStripItem)ScaleYAxisMenuItem,
			(ToolStripItem)ToolStripSeparator16,
			(ToolStripItem)ImportAxisMenuItem,
			(ToolStripItem)ToolStripSeparator11,
			(ToolStripItem)ClearChangedFlagToolStripMenuItem,
			(ToolStripItem)ToggleChangeFlagDisplayToolStripMenuItem,
			(ToolStripItem)ToolStripSeparator12,
			(ToolStripItem)ClearTableToZerosToolStripMenuItem,
			(ToolStripItem)ClearTableToNullsToolStripMenuItem,
			(ToolStripItem)ToolStripSeparator13,
			(ToolStripItem)ConvertZerosToNullsToolStripMenuItem,
			(ToolStripItem)ConvertNullsToZerosToolStripMenuItem
		});
		((ToolStripItem)OtherMenuItem).Name = "OtherMenuItem";
		ToolStripMenuItem otherMenuItem = OtherMenuItem;
		size = new Size(152, 22);
		((ToolStripItem)otherMenuItem).Size = size;
		((ToolStripItem)OtherMenuItem).Text = "Other";
		((ToolStripItem)TransposeClipboardToolStripMenuItem).Name = "TransposeClipboardToolStripMenuItem";
		ToolStripMenuItem transposeClipboardToolStripMenuItem = TransposeClipboardToolStripMenuItem;
		size = new Size(253, 22);
		((ToolStripItem)transposeClipboardToolStripMenuItem).Size = size;
		((ToolStripItem)TransposeClipboardToolStripMenuItem).Text = "Transpose Clipboard";
		((ToolStripItem)ToolStripSeparator15).Name = "ToolStripSeparator15";
		ToolStripSeparator toolStripSeparator10 = ToolStripSeparator15;
		size = new Size(250, 6);
		((ToolStripItem)toolStripSeparator10).Size = size;
		ToolStripTextBox2.BorderStyle = (BorderStyle)1;
		((ToolStripItem)ToolStripTextBox2).Name = "ToolStripTextBox2";
		ToolStripTextBox toolStripTextBox2 = ToolStripTextBox2;
		size = new Size(100, 23);
		((ToolStripControlHost)toolStripTextBox2).Size = size;
		((ToolStripControlHost)ToolStripTextBox2).Text = "1.0";
		((ToolStripItem)ScaleXAxisMenuItem).Name = "ScaleXAxisMenuItem";
		ToolStripMenuItem scaleXAxisMenuItem = ScaleXAxisMenuItem;
		size = new Size(253, 22);
		((ToolStripItem)scaleXAxisMenuItem).Size = size;
		((ToolStripItem)ScaleXAxisMenuItem).Text = "Scale Clipboard X-Axis Labels";
		((ToolStripItem)ScaleYAxisMenuItem).Name = "ScaleYAxisMenuItem";
		ToolStripMenuItem scaleYAxisMenuItem = ScaleYAxisMenuItem;
		size = new Size(253, 22);
		((ToolStripItem)scaleYAxisMenuItem).Size = size;
		((ToolStripItem)ScaleYAxisMenuItem).Text = "Scale Clipboard Y-Axis Labels";
		((ToolStripItem)ToolStripSeparator16).Name = "ToolStripSeparator16";
		ToolStripSeparator toolStripSeparator11 = ToolStripSeparator16;
		size = new Size(250, 6);
		((ToolStripItem)toolStripSeparator11).Size = size;
		((ToolStripItem)ImportAxisMenuItem).Name = "ImportAxisMenuItem";
		ToolStripMenuItem importAxisMenuItem = ImportAxisMenuItem;
		size = new Size(253, 22);
		((ToolStripItem)importAxisMenuItem).Size = size;
		((ToolStripItem)ImportAxisMenuItem).Text = "Import Table Axes from Clipboard";
		((ToolStripItem)ToolStripSeparator11).Name = "ToolStripSeparator11";
		ToolStripSeparator toolStripSeparator12 = ToolStripSeparator11;
		size = new Size(250, 6);
		((ToolStripItem)toolStripSeparator12).Size = size;
		((ToolStripItem)ClearChangedFlagToolStripMenuItem).Name = "ClearChangedFlagToolStripMenuItem";
		ToolStripMenuItem clearChangedFlagToolStripMenuItem = ClearChangedFlagToolStripMenuItem;
		size = new Size(253, 22);
		((ToolStripItem)clearChangedFlagToolStripMenuItem).Size = size;
		((ToolStripItem)ClearChangedFlagToolStripMenuItem).Text = "Clear Changed Flags";
		((ToolStripItem)ToggleChangeFlagDisplayToolStripMenuItem).Name = "ToggleChangeFlagDisplayToolStripMenuItem";
		ToolStripMenuItem toggleChangeFlagDisplayToolStripMenuItem = ToggleChangeFlagDisplayToolStripMenuItem;
		size = new Size(253, 22);
		((ToolStripItem)toggleChangeFlagDisplayToolStripMenuItem).Size = size;
		((ToolStripItem)ToggleChangeFlagDisplayToolStripMenuItem).Text = "Toggle Changed Flag Display";
		((ToolStripItem)ToolStripSeparator12).Name = "ToolStripSeparator12";
		ToolStripSeparator toolStripSeparator13 = ToolStripSeparator12;
		size = new Size(250, 6);
		((ToolStripItem)toolStripSeparator13).Size = size;
		((ToolStripItem)ClearTableToZerosToolStripMenuItem).Name = "ClearTableToZerosToolStripMenuItem";
		ToolStripMenuItem clearTableToZerosToolStripMenuItem = ClearTableToZerosToolStripMenuItem;
		size = new Size(253, 22);
		((ToolStripItem)clearTableToZerosToolStripMenuItem).Size = size;
		((ToolStripItem)ClearTableToZerosToolStripMenuItem).Text = "Clear Table to Zero's";
		((ToolStripItem)ClearTableToNullsToolStripMenuItem).Name = "ClearTableToNullsToolStripMenuItem";
		ToolStripMenuItem clearTableToNullsToolStripMenuItem = ClearTableToNullsToolStripMenuItem;
		size = new Size(253, 22);
		((ToolStripItem)clearTableToNullsToolStripMenuItem).Size = size;
		((ToolStripItem)ClearTableToNullsToolStripMenuItem).Text = "Clear Table to Null's";
		((ToolStripItem)ToolStripSeparator13).Name = "ToolStripSeparator13";
		ToolStripSeparator toolStripSeparator14 = ToolStripSeparator13;
		size = new Size(250, 6);
		((ToolStripItem)toolStripSeparator14).Size = size;
		((ToolStripItem)ConvertZerosToNullsToolStripMenuItem).Name = "ConvertZerosToNullsToolStripMenuItem";
		ToolStripMenuItem convertZerosToNullsToolStripMenuItem = ConvertZerosToNullsToolStripMenuItem;
		size = new Size(253, 22);
		((ToolStripItem)convertZerosToNullsToolStripMenuItem).Size = size;
		((ToolStripItem)ConvertZerosToNullsToolStripMenuItem).Text = "Convert Zero's to Null's";
		((ToolStripItem)ConvertNullsToZerosToolStripMenuItem).Name = "ConvertNullsToZerosToolStripMenuItem";
		ToolStripMenuItem convertNullsToZerosToolStripMenuItem = ConvertNullsToZerosToolStripMenuItem;
		size = new Size(253, 22);
		((ToolStripItem)convertNullsToZerosToolStripMenuItem).Size = size;
		((ToolStripItem)ConvertNullsToZerosToolStripMenuItem).Text = "Convert Null's to Zero's";
		((ToolStripItem)ToolStripSeparator2).Name = "ToolStripSeparator2";
		ToolStripSeparator toolStripSeparator15 = ToolStripSeparator2;
		size = new Size(149, 6);
		((ToolStripItem)toolStripSeparator15).Size = size;
		((ToolStripDropDownItem)GraphToolStripMenuItem).DropDownItems.AddRange((ToolStripItem[])(object)new ToolStripItem[2]
		{
			(ToolStripItem)Graph2DToolStripMenuItem,
			(ToolStripItem)Graph3DToolStripMenuItem
		});
		((ToolStripItem)GraphToolStripMenuItem).Name = "GraphToolStripMenuItem";
		ToolStripMenuItem graphToolStripMenuItem = GraphToolStripMenuItem;
		size = new Size(152, 22);
		((ToolStripItem)graphToolStripMenuItem).Size = size;
		((ToolStripItem)GraphToolStripMenuItem).Text = "Graph";
		((ToolStripItem)Graph2DToolStripMenuItem).Name = "Graph2DToolStripMenuItem";
		ToolStripMenuItem graph2DToolStripMenuItem = Graph2DToolStripMenuItem;
		size = new Size(123, 22);
		((ToolStripItem)graph2DToolStripMenuItem).Size = size;
		((ToolStripItem)Graph2DToolStripMenuItem).Text = "Graph 2D";
		((ToolStripItem)Graph3DToolStripMenuItem).Name = "Graph3DToolStripMenuItem";
		ToolStripMenuItem graph3DToolStripMenuItem = Graph3DToolStripMenuItem;
		size = new Size(123, 22);
		((ToolStripItem)graph3DToolStripMenuItem).Size = size;
		((ToolStripItem)Graph3DToolStripMenuItem).Text = "Graph 3D";
		((ToolStripItem)ToolbarToolStripMenuItem).Name = "ToolbarToolStripMenuItem";
		ToolStripMenuItem toolbarToolStripMenuItem = ToolbarToolStripMenuItem;
		size = new Size(152, 22);
		((ToolStripItem)toolbarToolStripMenuItem).Size = size;
		((ToolStripItem)ToolbarToolStripMenuItem).Text = "Toolbar";
		((ToolStripItem)ToolStripSeparator1).Name = "ToolStripSeparator1";
		ToolStripSeparator toolStripSeparator16 = ToolStripSeparator1;
		size = new Size(149, 6);
		((ToolStripItem)toolStripSeparator16).Size = size;
		UndoToolStripMenuItem.Enabled = false;
		((ToolStripItem)UndoToolStripMenuItem).Name = "UndoToolStripMenuItem";
		ToolStripMenuItem undoToolStripMenuItem = UndoToolStripMenuItem;
		size = new Size(152, 22);
		((ToolStripItem)undoToolStripMenuItem).Size = size;
		((ToolStripItem)UndoToolStripMenuItem).Text = "Undo";
		SizeF autoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleDimensions = autoScaleDimensions;
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Control)this).BackgroundImageLayout = (ImageLayout)0;
		((Control)this).ContextMenuStrip = DataMenuStrip;
		((Control)this).Controls.Add((Control)(object)TextBox1);
		((Control)this).DoubleBuffered = true;
		((Control)this).Name = "BCGridControl";
		size = new Size(285, 289);
		((Control)this).Size = size;
		((Control)DataMenuStrip).ResumeLayout(false);
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}

	private void BCGridControl_Load(object sender, EventArgs e)
	{
		//IL_00a7: Unknown result type (might be due to invalid IL or missing references)
		//IL_00ad: Expected O, but got Unknown
		if (Operators.CompareString(m_Grid_VisibleName, "", false) == 0)
		{
			m_Grid_VisibleName = ((Control)this).Name;
		}
		Graph.Text = m_Grid_VisibleName;
		Graph.BackColor = Color.WhiteSmoke;
		((Control)Graph).Width = 400;
		((Control)Graph).Height = 400;
		Toolbar.Text = m_Grid_VisibleName;
		Toolbar.FormBorderStyle = (FormBorderStyle)5;
		Toolbar.TopMost = true;
		((Control)Toolbar).Width = 465;
		((Control)Toolbar).Height = 50;
		ToolTip val = new ToolTip();
		val.ShowAlways = true;
		TextBox tB_Text = TB_Text1;
		Point location = new Point(3, 3);
		((Control)tB_Text).Location = location;
		((Control)Toolbar).Controls.Add((Control)(object)TB_Text1);
		Button tB_Btn = TB_Btn1;
		location = new Point(105, 3);
		((Control)tB_Btn).Location = location;
		Button tB_Btn2 = TB_Btn1;
		Size size = new Size(20, 20);
		((Control)tB_Btn2).Size = size;
		((ButtonBase)TB_Btn1).Text = "=";
		((Control)Toolbar).Controls.Add((Control)(object)TB_Btn1);
		val.SetToolTip((Control)(object)TB_Btn1, "Fill");
		Button tB_Btn3 = TB_Btn2;
		location = new Point(125, 3);
		((Control)tB_Btn3).Location = location;
		Button tB_Btn4 = TB_Btn2;
		size = new Size(20, 20);
		((Control)tB_Btn4).Size = size;
		((ButtonBase)TB_Btn2).Text = "+";
		((Control)Toolbar).Controls.Add((Control)(object)TB_Btn2);
		val.SetToolTip((Control)(object)TB_Btn2, "Add");
		Button tB_Btn5 = TB_Btn3;
		location = new Point(145, 3);
		((Control)tB_Btn5).Location = location;
		Button tB_Btn6 = TB_Btn3;
		size = new Size(20, 20);
		((Control)tB_Btn6).Size = size;
		((ButtonBase)TB_Btn3).Text = "-";
		((Control)Toolbar).Controls.Add((Control)(object)TB_Btn3);
		val.SetToolTip((Control)(object)TB_Btn3, "Subtract");
		Button tB_Btn7 = TB_Btn4;
		location = new Point(165, 3);
		((Control)tB_Btn7).Location = location;
		Button tB_Btn8 = TB_Btn4;
		size = new Size(20, 20);
		((Control)tB_Btn8).Size = size;
		((ButtonBase)TB_Btn4).Text = "*";
		((Control)Toolbar).Controls.Add((Control)(object)TB_Btn4);
		val.SetToolTip((Control)(object)TB_Btn4, "Multiply");
		Button tB_Btn9 = TB_Btn5;
		location = new Point(185, 3);
		((Control)tB_Btn9).Location = location;
		Button tB_Btn10 = TB_Btn5;
		size = new Size(20, 20);
		((Control)tB_Btn10).Size = size;
		((ButtonBase)TB_Btn5).Text = "/";
		((Control)Toolbar).Controls.Add((Control)(object)TB_Btn5);
		val.SetToolTip((Control)(object)TB_Btn5, "Divide");
		Button tB_Btn11 = TB_Btn6;
		location = new Point(210, 3);
		((Control)tB_Btn11).Location = location;
		Button tB_Btn12 = TB_Btn6;
		size = new Size(30, 20);
		((Control)tB_Btn12).Size = size;
		((ButtonBase)TB_Btn6).Text = "S";
		((Control)Toolbar).Controls.Add((Control)(object)TB_Btn6);
		val.SetToolTip((Control)(object)TB_Btn6, "Smooth");
		Button tB_Btn13 = TB_Btn7;
		location = new Point(240, 3);
		((Control)tB_Btn13).Location = location;
		Button tB_Btn14 = TB_Btn7;
		size = new Size(30, 20);
		((Control)tB_Btn14).Size = size;
		((ButtonBase)TB_Btn7).Text = "SH";
		((Control)Toolbar).Controls.Add((Control)(object)TB_Btn7);
		val.SetToolTip((Control)(object)TB_Btn7, "Smooth Horizontal");
		Button tB_Btn15 = TB_Btn8;
		location = new Point(270, 3);
		((Control)tB_Btn15).Location = location;
		Button tB_Btn16 = TB_Btn8;
		size = new Size(30, 20);
		((Control)tB_Btn16).Size = size;
		((ButtonBase)TB_Btn8).Text = "SV";
		((Control)Toolbar).Controls.Add((Control)(object)TB_Btn8);
		val.SetToolTip((Control)(object)TB_Btn8, "Smooth Vertical");
		Button tB_Btn17 = TB_Btn9;
		location = new Point(305, 3);
		((Control)tB_Btn17).Location = location;
		Button tB_Btn18 = TB_Btn9;
		size = new Size(30, 20);
		((Control)tB_Btn18).Size = size;
		((ButtonBase)TB_Btn9).Text = "I";
		((Control)Toolbar).Controls.Add((Control)(object)TB_Btn9);
		val.SetToolTip((Control)(object)TB_Btn9, "Interpolate");
		Button tB_Btn19 = TB_Btn10;
		location = new Point(335, 3);
		((Control)tB_Btn19).Location = location;
		Button tB_Btn20 = TB_Btn10;
		size = new Size(30, 20);
		((Control)tB_Btn20).Size = size;
		((ButtonBase)TB_Btn10).Text = "IH";
		((Control)Toolbar).Controls.Add((Control)(object)TB_Btn10);
		val.SetToolTip((Control)(object)TB_Btn10, "Interpolate Horizontal");
		Button tB_Btn21 = TB_Btn11;
		location = new Point(365, 3);
		((Control)tB_Btn21).Location = location;
		Button tB_Btn22 = TB_Btn11;
		size = new Size(30, 20);
		((Control)tB_Btn22).Size = size;
		((ButtonBase)TB_Btn11).Text = "IV";
		((Control)Toolbar).Controls.Add((Control)(object)TB_Btn11);
		val.SetToolTip((Control)(object)TB_Btn11, "Interpolate Vertical");
		Button tB_Btn23 = TB_Btn12;
		location = new Point(400, 3);
		((Control)tB_Btn23).Location = location;
		Button tB_Btn24 = TB_Btn12;
		size = new Size(30, 20);
		((Control)tB_Btn24).Size = size;
		((ButtonBase)TB_Btn12).Text = "E";
		((Control)Toolbar).Controls.Add((Control)(object)TB_Btn12);
		val.SetToolTip((Control)(object)TB_Btn12, "Extrapolate");
		Button tB_Btn25 = TB_Btn13;
		location = new Point(435, 3);
		((Control)tB_Btn25).Location = location;
		Button tB_Btn26 = TB_Btn13;
		size = new Size(20, 20);
		((Control)tB_Btn26).Size = size;
		((ButtonBase)TB_Btn13).Text = "U";
		((Control)TB_Btn13).Enabled = false;
		((Control)Toolbar).Controls.Add((Control)(object)TB_Btn13);
		val.SetToolTip((Control)(object)TB_Btn13, "Undo");
		ReSize_Data();
		IsDrawling = 0;
		IsDrawlingG = 0;
		Init = 1;
		Draw_Grid();
	}

	private void ReSize_Data()
	{
		checked
		{
			Busy++;
			if (m_Grid_X < 1)
			{
				m_Grid_X = 1;
			}
			if (m_Grid_X > MAX_X)
			{
				m_Grid_X = MAX_X;
			}
			if (m_Grid_Y < 1)
			{
				m_Grid_Y = 1;
			}
			if (m_Grid_Y > MAX_Y)
			{
				m_Grid_Y = MAX_Y;
			}
			GData = new float[1 + (m_Grid_X + 1) * (m_Grid_Y + 1) + 1];
			SData = new byte[1 + (m_Grid_X + 1) * (m_Grid_Y + 1) + 1];
			GDataU = new float[1 + (m_Grid_X + 1) * (m_Grid_Y + 1) * MAX_U + 1];
			Clear_Changed_Flags();
			ClearUndo();
			LX = 1;
			LY = 1;
			L2X = -1;
			L2Y = -1;
			GMSX = 1;
			GMSY = 1;
			ReSize_Grid();
			Busy--;
			if (Busy < 0)
			{
				Busy = 0;
			}
		}
	}

	private void ReSize_Grid()
	{
		checked
		{
			Busy++;
			Check_Width();
			if (m_Grid_Transpose == 0)
			{
				((Control)this).Width = (m_Grid_X + m_Grid_ShowLabels) * m_Cell_W + 1;
				((Control)this).Height = (m_Grid_Y + m_Grid_ShowLabels) * m_Cell_H + 1;
			}
			else
			{
				((Control)this).Width = (m_Grid_Y + m_Grid_ShowLabels) * m_Cell_W + 1;
				((Control)this).Height = (m_Grid_X + m_Grid_ShowLabels) * m_Cell_H + 1;
			}
			m_Grid_ReDraw = 1;
			Busy--;
			if (Busy < 0)
			{
				Busy = 0;
			}
		}
	}

	private void Timer1_Tick(object sender, EventArgs e)
	{
		checked
		{
			if (Init != 0)
			{
				Point point = default(Point);
				point = ((Control)this).Parent.PointToScreen(((Control)this).Location);
				Mouse_Over = 0;
				if (((Control)this).Visible & (Cursor.Position.X >= point.X) & (Cursor.Position.X <= point.X + ((Control)this).Width) & (Cursor.Position.Y >= point.Y) & (Cursor.Position.Y <= point.Y + ((Control)this).Height))
				{
					Mouse_Over = 1;
				}
				if (((Control)Toolbar).Visible & (Cursor.Position.X >= ((Control)Toolbar).Left) & (Cursor.Position.X <= ((Control)Toolbar).Left + ((Control)Toolbar).Width) & (Cursor.Position.Y >= ((Control)Toolbar).Top) & (Cursor.Position.Y <= ((Control)Toolbar).Top + ((Control)Toolbar).Height))
				{
					Mouse_Over = 1;
				}
				if (((Control)Graph).Visible & (Cursor.Position.X >= ((Control)Graph).Left) & (Cursor.Position.X <= ((Control)Graph).Left + ((Control)Graph).Width) & (Cursor.Position.Y >= ((Control)Graph).Top) & (Cursor.Position.Y <= ((Control)Graph).Top + ((Control)Graph).Height))
				{
					Mouse_Over = 1;
				}
				if (Mouse_Over != Mouse_OverP)
				{
					Mouse_OverP = Mouse_Over;
					m_Grid_ReDraw = 1;
				}
				Check_Focus();
				if (m_Grid_ReDraw == 1)
				{
					Draw_Grid();
				}
			}
		}
	}

	private void BCGridControl_Resize(object sender, EventArgs e)
	{
		ReSize_Grid();
	}

	private void BCGridControl_VisibleChanged(object sender, EventArgs e)
	{
		if (!((Control)this).Visible)
		{
			((Control)Graph).Hide();
			((Control)Toolbar).Hide();
		}
	}

	private void Check_Focus()
	{
		DFocus = 0;
		if (((Control)this).Focused | ((Control)Graph).Focused | ((Control)Toolbar).Focused | ((Control)TB_Text1).Focused | ((Control)TB_Btn1).Focused | ((Control)TB_Btn2).Focused | ((Control)TB_Btn3).Focused | ((Control)TB_Btn4).Focused | ((Control)TB_Btn5).Focused | ((Control)TB_Btn6).Focused | ((Control)TB_Btn7).Focused | ((Control)TB_Btn8).Focused | ((Control)TB_Btn9).Focused | ((Control)TB_Btn10).Focused | ((Control)TB_Btn11).Focused | ((Control)TB_Btn12).Focused | ((Control)TB_Btn13).Focused)
		{
			DFocus = 1;
		}
		if ((Mouse_Over == 1) & (DFocus == 0))
		{
			DFocus = 2;
		}
		if (DFocus != DFocusP)
		{
			if (DFocus != 1)
			{
				((Control)Toolbar).Hide();
			}
			DFocusP = DFocus;
			m_Grid_ReDraw = 1;
		}
	}

	private void Check_Width()
	{
		if (Cell_Auto_W == 1)
		{
			m_Cell_W = checked(m_Cell_CharMax * 8);
			if (m_Cell_W < 16)
			{
				m_Cell_W = 16;
			}
			if (m_Cell_W > 80)
			{
				m_Cell_W = 80;
			}
		}
	}

	public void Wait()
	{
		while (Busy != 0)
		{
		}
	}

	public void W_Data(byte X, byte Y, float D)
	{
		if (Init != 0)
		{
			GData[checked(X + Y * (m_Grid_X + 1))] = D;
			m_Grid_ReDraw = 1;
		}
	}

	public float R_Data(byte X, byte Y)
	{
		if (Init == 0)
		{
			return 0f;
		}
		return GData[checked(X + Y * (m_Grid_X + 1))];
	}

	public float L_Data(float LUX, float LUY)
	{
		if (Init == 0)
		{
			return 0f;
		}
		int num = 0;
		int num2 = 0;
		float num3 = 0f;
		float num4 = 0f;
		float num5 = 0f;
		float num6 = 0f;
		float num7 = 0f;
		if (m_Grid_ShowLabels != 1)
		{
			return 100000000f;
		}
		checked
		{
			int num8 = m_Grid_X - 1;
			num = 1;
			while (true)
			{
				if (num <= num8)
				{
					if ((LUX >= GData[num + 0 * (m_Grid_X + 1)]) & (LUX <= GData[num + 1 + 0 * (m_Grid_X + 1)]))
					{
						break;
					}
					num++;
					continue;
				}
				return 100000000f;
			}
			int num9 = m_Grid_Y - 1;
			num2 = 1;
			while (true)
			{
				if (num2 <= num9)
				{
					if ((LUY >= GData[0 + num2 * (m_Grid_X + 1)]) & (LUY <= GData[0 + (num2 + 1) * (m_Grid_X + 1)]))
					{
						break;
					}
					num2++;
					continue;
				}
				return 100000000f;
			}
			if ((GData[num + num2 * (m_Grid_X + 1)] >= 100000000f) | (GData[num + 1 + num2 * (m_Grid_X + 1)] >= 100000000f) | (GData[num + (num2 + 1) * (m_Grid_X + 1)] >= 100000000f) | (GData[num + 1 + (num2 + 1) * (m_Grid_X + 1)] >= 100000000f))
			{
				return 100000000f;
			}
			if (GData[num + 1 + 0 * (m_Grid_X + 1)] - GData[num + 0 * (m_Grid_X + 1)] == 0f)
			{
				return 0f;
			}
			if (GData[0 + (num2 + 1) * (m_Grid_X + 1)] - GData[0 + num2 * (m_Grid_X + 1)] == 0f)
			{
				return 0f;
			}
			num6 = (LUX - GData[num + 0 * (m_Grid_X + 1)]) / (GData[num + 1 + 0 * (m_Grid_X + 1)] - GData[num + 0 * (m_Grid_X + 1)]);
			num7 = (LUY - GData[0 + num2 * (m_Grid_X + 1)]) / (GData[0 + (num2 + 1) * (m_Grid_X + 1)] - GData[0 + num2 * (m_Grid_X + 1)]);
			num4 = GData[num + num2 * (m_Grid_X + 1)] + (GData[num + (num2 + 1) * (m_Grid_X + 1)] - GData[num + num2 * (m_Grid_X + 1)]) * num7;
			num5 = GData[num + 1 + num2 * (m_Grid_X + 1)] + (GData[num + 1 + (num2 + 1) * (m_Grid_X + 1)] - GData[num + 1 + num2 * (m_Grid_X + 1)]) * num7;
			return num4 + (num5 - num4) * num6;
		}
	}

	private void Draw_Grid()
	{
		//IL_006a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0070: Expected O, but got Unknown
		Wait();
		if (m_Grid_FreezeDraw == 1 || IsDrawling == 1)
		{
			return;
		}
		IsDrawling = 1;
		checked
		{
			if ((L2X == -1) & (L2Y == -1))
			{
				m_Grid_DataStatus++;
			}
			if (m_Grid_DataStatus >= 30000)
			{
				m_Grid_DataStatus = 0;
			}
			Check_Focus();
			Bitmap val = new Bitmap(((Control)this).Width, ((Control)this).Height);
			Graphics val2 = Graphics.FromImage((Image)(object)val);
			float num = -100000000f;
			float num2 = 100000000f;
			float num3 = 1f;
			int num4 = 255;
			int num5 = 255;
			int num6 = 255;
			int grid_X = m_Grid_X;
			for (int i = 1; i <= grid_X; i++)
			{
				int grid_Y = m_Grid_Y;
				for (int j = 1; j <= grid_Y; j++)
				{
					float num7 = GData[i + j * (m_Grid_X + 1)];
					if (!(num7 >= 100000000f))
					{
						if (num7 < num2)
						{
							num2 = num7;
						}
						if (num7 > num)
						{
							num = num7;
						}
					}
				}
			}
			int num8 = 1 - m_Grid_ShowLabels;
			int grid_X2 = m_Grid_X;
			for (int i = num8; i <= grid_X2; i++)
			{
				int num9 = 1 - m_Grid_ShowLabels;
				int grid_Y2 = m_Grid_Y;
				for (int j = num9; j <= grid_Y2; j++)
				{
					float num10 = GData[i + j * (m_Grid_X + 1)];
					string text;
					unchecked
					{
						if (m_Grid_ShowLabels == 1 && (i == 0 || j == 0))
						{
							C_Brush.Color = ((Control)this).BackColor;
							C_Pen.Color = ((Control)this).BackColor;
							if (i == 0 && j == 0)
							{
								T_Brush.Color = ((Control)this).BackColor;
							}
							else
							{
								T_Brush.Color = ((Control)this).ForeColor;
							}
							text = Strings.Format((object)num10, m_Cell_LabelFormat);
						}
						else
						{
							num3 = ((!(num10 >= 100000000f)) ? ((float)((double)(num10 - num2) / ((double)num + 0.0001 - (double)num2))) : 0f);
							checked
							{
								if ((((SData[i + j * (m_Grid_X + 1)] & 1) | (SData[i + j * (m_Grid_X + 1)] & 2)) & unchecked(0 - ((DFocus > 0) ? 1 : 0))) != 0)
								{
									num4 = (int)Math.Round((float)unchecked((int)m_Cell_LSelCLR.R) + (float)(m_Cell_HSelCLR.R - m_Cell_LSelCLR.R) * num3);
									num5 = (int)Math.Round((float)unchecked((int)m_Cell_LSelCLR.G) + (float)(m_Cell_HSelCLR.G - m_Cell_LSelCLR.G) * num3);
									num6 = (int)Math.Round((float)unchecked((int)m_Cell_LSelCLR.B) + (float)(m_Cell_HSelCLR.B - m_Cell_LSelCLR.B) * num3);
									T_Brush.Color = m_Cell_FSelCLR;
								}
								else
								{
									num4 = (int)Math.Round((float)unchecked((int)m_Cell_LowCLR.R) + (float)(m_Cell_HighCLR.R - m_Cell_LowCLR.R) * num3);
									num5 = (int)Math.Round((float)unchecked((int)m_Cell_LowCLR.G) + (float)(m_Cell_HighCLR.G - m_Cell_LowCLR.G) * num3);
									num6 = (int)Math.Round((float)unchecked((int)m_Cell_LowCLR.B) + (float)(m_Cell_HighCLR.B - m_Cell_LowCLR.B) * num3);
									T_Brush.Color = m_Cell_FontCLR;
								}
								if (num4 < 0)
								{
									num4 = 0;
									if (num5 < 0)
									{
										num5 = 0;
										if (num6 < 0)
										{
											num6 = 0;
										}
									}
								}
								if (num4 > 255)
								{
									num4 = 255;
									if (num5 > 255)
									{
										num5 = 255;
										if (num6 > 255)
										{
											num6 = 255;
										}
									}
								}
								C_Brush.Color = Color.FromArgb(num4, num5, num6);
								C_Pen.Color = Color.Black;
								T_Pen.Color = Color.Gray;
								text = Strings.Format((object)(num10 * m_Grid_DataScalar + m_Grid_DataOffset), m_Cell_Format);
							}
						}
						text = Strings.Mid(text, 1, (int)m_Cell_CharMax);
						if (num10 >= 100000000f)
						{
							text = "";
						}
					}
					int num11;
					int num12;
					if (m_Grid_Transpose == 0)
					{
						num11 = (i - 1 + m_Grid_ShowLabels) * m_Cell_W;
						num12 = (j - 1 + m_Grid_ShowLabels) * m_Cell_H;
					}
					else
					{
						num11 = (j - 1 + m_Grid_ShowLabels) * m_Cell_W;
						num12 = (i - 1 + m_Grid_ShowLabels) * m_Cell_H;
					}
					val2.FillRectangle((Brush)(object)C_Brush, num11, num12, m_Cell_W, m_Cell_H);
					val2.DrawRectangle(C_Pen, num11, num12, m_Cell_W, m_Cell_H);
					if ((SData[i + j * (m_Grid_X + 1)] & 8 & unchecked(0 - ((m_Cell_ShowChanges == 1) ? 1 : 0))) != 0)
					{
						val2.DrawRectangle(T_Pen, num11 + 1, num12 + 1, m_Cell_W - 2, m_Cell_H - 2);
					}
					if ((i == LX) & (j == LY) & (DFocus > 0))
					{
						val2.DrawRectangle(C_Pen, num11 + 1, num12 + 1, m_Cell_W - 2, m_Cell_H - 2);
					}
					val2.DrawString(text, ((Control)this).Font, (Brush)(object)T_Brush, (float)num11, (float)num12);
				}
			}
			((Control)this).BackgroundImage = (Image)(object)val;
			((Control)this).Refresh();
			IsDrawling = 0;
			m_Grid_ReDraw = 0;
			if (((Control)Graph).Visible)
			{
				Draw_Graph();
			}
		}
	}

	private void Draw_Graph()
	{
		//IL_00d8: Unknown result type (might be due to invalid IL or missing references)
		//IL_00de: Expected O, but got Unknown
		//IL_007a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0084: Expected O, but got Unknown
		Wait();
		if (m_Grid_FreezeDraw == 1 || IsDrawlingG == 1)
		{
			return;
		}
		IsDrawlingG = 1;
		Form graph = Graph;
		Size minimumSize = new Size(200, 200);
		graph.MinimumSize = minimumSize;
		if ((Graph.ClientSize.Width < 125) | (Graph.ClientSize.Height < 125))
		{
			((Control)Graph).BackgroundImage = (Image)new Bitmap(1, 1);
			IsDrawlingG = 0;
			return;
		}
		float num = -100000000f;
		float num2 = 100000000f;
		int num3 = 50;
		int num4 = 255;
		int num5 = 255;
		int num6 = 255;
		Bitmap val = new Bitmap(Graph.ClientSize.Width, Graph.ClientSize.Height);
		Graphics val2 = Graphics.FromImage((Image)(object)val);
		int grid_X = m_Grid_X;
		checked
		{
			for (int i = 1; i <= grid_X; i++)
			{
				int grid_Y = m_Grid_Y;
				for (int j = 1; j <= grid_Y; j++)
				{
					double num7 = GData[i + j * (m_Grid_X + 1)];
					if (!(num7 >= 99999998.0))
					{
						if (num7 < (double)num2)
						{
							num2 = (float)num7;
						}
						if (num7 > (double)num)
						{
							num = (float)num7;
						}
					}
				}
			}
			T_Brush.Color = ((Control)this).ForeColor;
			C_Brush.Color = Graph.BackColor;
			val2.FillRectangle((Brush)(object)C_Brush, 1, 1, ((Image)val).Width, ((Image)val).Height);
			if (m_Grid_GraphType == 1)
			{
				int num8 = ((Image)val).Width - num3 * 2;
				int num9 = ((Image)val).Height - num3 * 2;
				C_Pen.Color = Color.Black;
				double num10 = (int)Math.Round((double)num9 / 20.0);
				num10 = (double)(num - num2) / num10;
				if (num10 < 0.01)
				{
					num10 = 1.0;
				}
				double num11 = num2;
				double num12 = num;
				double num13 = num10;
				double num14 = num12;
				for (double num7 = num11; ForLoopControl.ForNextCheckR8(num7, num14, num13); num7 += num13)
				{
					float num15 = (float)((num7 - (double)num2) / ((double)num + 0.0001 - (double)num2));
					val2.DrawLine(C_Pen, (float)(num3 - 10), (float)num3 + (float)num9 * (1f - num15), (float)num3, (float)num3 + (float)num9 * (1f - num15));
					val2.DrawString(AutoFormat((float)(num7 * (double)m_Grid_DataScalar + (double)m_Grid_DataOffset)), ((Control)this).Font, (Brush)(object)T_Brush, 4f, (float)num3 + (float)num9 * (1f - num15) - 5f);
				}
				val2.DrawLine(C_Pen, num3, num3, num3, num3 + num9);
				int grid_X2 = m_Grid_X;
				for (int i = 1; i <= grid_X2; i++)
				{
					float num15 = (float)((double)(i - 1) / (double)(m_Grid_X - 1));
					val2.DrawLine(C_Pen, (float)num3 + (float)num8 * num15, (float)(num3 + num9), (float)num3 + (float)num8 * num15, (float)(num3 + num9 + 10));
					if (m_Grid_ShowLabels == 1)
					{
						string text = AutoFormat(GData[i + 0 * (m_Grid_X + 1)]);
						if ((double)num8 / (double)m_Grid_X > (double)((Strings.Len(text) - 1) * 8))
						{
							val2.DrawString(text, ((Control)this).Font, (Brush)(object)T_Brush, (float)num3 + (float)num8 * num15 - (float)(Strings.Len(text) * 4), (float)(num3 + num9 + 15));
						}
					}
				}
				val2.DrawLine(C_Pen, num3, num3 + num9, num3 + num8, num3 + num9);
				GMD = 100000000;
				int grid_Y2 = m_Grid_Y;
				for (int j = 1; j <= grid_Y2; j++)
				{
					switch (j)
					{
					case 1:
						num4 = 200;
						num5 = 0;
						num6 = 0;
						break;
					case 2:
						num4 = 0;
						num5 = 200;
						num6 = 0;
						break;
					case 3:
						num4 = 0;
						num5 = 0;
						num6 = 200;
						break;
					case 4:
						num4 = 200;
						num5 = 200;
						num6 = 0;
						break;
					case 5:
						num4 = 200;
						num5 = 0;
						num6 = 200;
						break;
					case 6:
						num4 = 0;
						num5 = 200;
						num6 = 200;
						break;
					case 7:
						num4 = 100;
						num5 = 0;
						num6 = 0;
						break;
					case 8:
						num4 = 0;
						num5 = 100;
						num6 = 0;
						break;
					case 9:
						num4 = 0;
						num5 = 0;
						num6 = 100;
						break;
					case 10:
						num4 = 100;
						num5 = 100;
						num6 = 0;
						break;
					case 11:
						num4 = 100;
						num5 = 0;
						num6 = 100;
						break;
					case 12:
						num4 = 0;
						num5 = 100;
						num6 = 100;
						break;
					default:
						num4 = 0;
						num5 = 0;
						num6 = 0;
						break;
					}
					C_Pen.Color = Color.FromArgb(num4, num5, num6);
					if (m_Grid_ShowLabels == 1)
					{
						string text = AutoFormat(GData[0 + j * (m_Grid_X + 1)]);
						val2.DrawLine(C_Pen, num3 + num8 + 5, num3 + (j - 1) * 25, num3 + num8 + num3 - 5, num3 + (j - 1) * 25);
						val2.DrawString(text, ((Control)this).Font, (Brush)(object)T_Brush, (float)(num3 + num8 + 5), (float)(num3 + (j - 1) * 25 - 12));
					}
					int num16 = -1;
					int num17 = -1;
					int grid_X3 = m_Grid_X;
					for (int i = 1; i <= grid_X3; i++)
					{
						double num7 = (double)(i - 1) / (double)(m_Grid_X - 1);
						int num18 = (int)Math.Round((double)num8 * num7);
						num7 = GData[i + j * (m_Grid_X + 1)];
						if (num7 < 99999998.0)
						{
							num7 = (num7 - (double)num2) / ((double)num + 0.0001 - (double)num2);
							int num19 = (int)Math.Round((double)num9 * num7);
							num18 += num3;
							num19 = ((Image)val).Height - num3 - num19;
							if ((Math.Sqrt(Math.Pow(num18 - GMX, 2.0) + Math.Pow(num19 - GMY, 2.0)) < (double)GMD) & (GMB == 0))
							{
								GMD = (int)Math.Round(Math.Sqrt(Math.Pow(num18 - GMX, 2.0) + Math.Pow(num19 - GMY, 2.0)));
								GMSX = i;
								GMSY = j;
								GMSS = (num - num2) / (float)num9;
								if (GMSS == 0f)
								{
									GMSS = 0.1f;
								}
							}
							val2.DrawRectangle(C_Pen, num18 - 2, num19 - 2, 4, 4);
							if (unchecked(num16 >= 0 && num17 >= 0))
							{
								val2.DrawLine(C_Pen, num18, num19, num16, num17);
							}
							num16 = num18;
							num17 = num19;
						}
						else
						{
							num16 = -1;
							num17 = -1;
						}
					}
				}
			}
			else if (m_Grid_GraphType == 2)
			{
				float[,] array = new float[1 + (m_Grid_X + 1) * (m_Grid_Y + 1) + 1, 4];
				float[,] array2 = new float[1 + (m_Grid_X + 1) * (m_Grid_Y + 1) + 1, 6];
				float[] array3 = new float[6];
				PointF[] array4 = new PointF[4];
				float num20 = (float)((double)((Image)val).Width / 2.0);
				float num21 = (float)((double)((Image)val).Height / 2.0);
				float num22 = (num20 + num21) / 2f;
				byte b;
				float num23;
				float num24;
				float num25;
				float num26;
				float num27;
				float num28;
				if ((GData[m_Grid_X + 0 * (m_Grid_X + 1)] > GData[1 + 0 * (m_Grid_X + 1)]) & (GData[0 + m_Grid_Y * (m_Grid_X + 1)] > GData[0 + 1 * (m_Grid_X + 1)]) & (m_Grid_ShowLabels == 1))
				{
					b = 1;
					num23 = 1000f / (GData[m_Grid_X + 0 * (m_Grid_X + 1)] - GData[1 + 0 * (m_Grid_X + 1)]);
					num24 = GData[1 + 0 * (m_Grid_X + 1)] + (GData[m_Grid_X + 0 * (m_Grid_X + 1)] - GData[1 + 0 * (m_Grid_X + 1)]) / 2f;
					num25 = (float)(1000.0 / ((double)(num - num2) + 0.01));
					num26 = num2 + (num - num2) / 2f;
					num27 = 1000f / (GData[0 + m_Grid_Y * (m_Grid_X + 1)] - GData[0 + 1 * (m_Grid_X + 1)]);
					num28 = GData[0 + 1 * (m_Grid_X + 1)] + (GData[0 + m_Grid_Y * (m_Grid_X + 1)] - GData[0 + 1 * (m_Grid_X + 1)]) / 2f;
				}
				else
				{
					b = 0;
					num23 = (float)(1000.0 / (double)(m_Grid_X - 1));
					num24 = (float)((double)m_Grid_X / 2.0);
					num25 = (float)(1000.0 / ((double)(num - num2) + 0.01));
					num26 = num2 + (num - num2) / 2f;
					num27 = (float)(1000.0 / (double)(m_Grid_Y - 1));
					num28 = (float)((double)m_Grid_Y / 2.0);
				}
				GMD = 100000000;
				int grid_X4 = m_Grid_X;
				int l;
				for (int k = 1; k <= grid_X4; k++)
				{
					int grid_Y3 = m_Grid_Y;
					for (l = 1; l <= grid_Y3; l++)
					{
						float num29;
						float num30;
						if (b == 1)
						{
							num29 = (GData[k + 0 * (m_Grid_X + 1)] - num24) * (0f - num23);
							num30 = (GData[0 + l * (m_Grid_X + 1)] - num28) * num27;
						}
						else
						{
							num29 = ((float)k - num24) * (0f - num23);
							num30 = ((float)l - num28) * num27;
						}
						if (GData[k + l * (m_Grid_X + 1)] < 100000000f)
						{
							float num31 = (GData[k + l * (m_Grid_X + 1)] - num26) * (0f - num25);
							float num32 = (float)((double)num29 * Math.Cos(ZD) - (double)num31 * Math.Sin(ZD));
							float num33 = (float)((double)num31 * Math.Cos(ZD) + (double)num29 * Math.Sin(ZD));
							float num34 = (float)((double)num30 * Math.Cos(XD) + (double)num33 * Math.Sin(XD));
							num31 = (float)((double)num33 * Math.Cos(XD) - (double)num30 * Math.Sin(XD));
							num29 = (float)((double)num32 * Math.Cos(YD) - (double)num34 * Math.Sin(YD));
							num30 = (float)((double)num34 * Math.Cos(YD) + (double)num32 * Math.Sin(YD));
							array[k + l * (m_Grid_X + 1), 1] = (float)((double)num20 + (double)(num29 + VW_X) / ((double)(num30 - VW_Z) + 1E-05) * (double)num22 * (double)VW_ZM);
							array[k + l * (m_Grid_X + 1), 2] = (float)((double)num21 + (double)(num31 + VW_Y) / ((double)(num30 - VW_Z) + 1E-05) * (double)num22 * (double)VW_ZM);
							array[k + l * (m_Grid_X + 1), 0] = (float)Math.Sqrt(Math.Pow(num29 - VW_X, 2.0) + Math.Pow(num31 - VW_Y, 2.0) + Math.Pow(num30 - VW_Z, 2.0));
							array[k + l * (m_Grid_X + 1), 3] = (float)((double)(GData[k + l * (m_Grid_X + 1)] - num2) / ((double)num + 0.0001 - (double)num2));
							if ((Math.Sqrt(Math.Pow(array[k + l * (m_Grid_X + 1), 1] - (float)GMX, 2.0) + Math.Pow(array[k + l * (m_Grid_X + 1), 2] - (float)GMY, 2.0)) < (double)GMD) & (GMB == 0))
							{
								GMD = (int)Math.Round(Math.Sqrt(Math.Pow(array[k + l * (m_Grid_X + 1), 1] - (float)GMX, 2.0) + Math.Pow(array[k + l * (m_Grid_X + 1), 2] - (float)GMY, 2.0)));
								GMSX = k;
								GMSY = l;
								GMSS = (num - num2) / num22;
								if (GMSS == 0f)
								{
									GMSS = 0.1f;
								}
							}
						}
						else
						{
							array[k + l * (m_Grid_X + 1), 1] = num20;
							array[k + l * (m_Grid_X + 1), 2] = num21;
							array[k + l * (m_Grid_X + 1), 0] = 0f;
							array[k + l * (m_Grid_X + 1), 3] = 0f;
						}
					}
				}
				array2[0, 0] = 0f;
				int num35 = m_Grid_X - 1;
				for (int k = 1; k <= num35; k++)
				{
					int num36 = m_Grid_Y - 1;
					for (l = 1; l <= num36; l++)
					{
						if ((array[k + l * (m_Grid_X + 1), 0] != 0f) & (array[k + 1 + l * (m_Grid_X + 1), 0] != 0f) & (array[k + (l + 1) * (m_Grid_X + 1), 0] != 0f) & (array[k + 1 + (l + 1) * (m_Grid_X + 1), 0] != 0f))
						{
							array2[0, 0] += 1f;
							array2[(int)Math.Round(array2[0, 0]), 0] = (array[k + l * (m_Grid_X + 1), 0] + array[k + 1 + l * (m_Grid_X + 1), 0] + array[k + (l + 1) * (m_Grid_X + 1), 0] + array[k + 1 + (l + 1) * (m_Grid_X + 1), 0]) / 4f;
							array2[(int)Math.Round(array2[0, 0]), 5] = array[k + l * (m_Grid_X + 1), 3];
							if (array2[(int)Math.Round(array2[0, 0]), 5] < array[k + (l + 1) * (m_Grid_X + 1), 3])
							{
								array2[(int)Math.Round(array2[0, 0]), 5] = array[k + (l + 1) * (m_Grid_X + 1), 3];
							}
							if (array2[(int)Math.Round(array2[0, 0]), 5] < array[k + 1 + (l + 1) * (m_Grid_X + 1), 3])
							{
								array2[(int)Math.Round(array2[0, 0]), 5] = array[k + 1 + (l + 1) * (m_Grid_X + 1), 3];
							}
							if (array2[(int)Math.Round(array2[0, 0]), 5] < array[k + 1 + l * (m_Grid_X + 1), 3])
							{
								array2[(int)Math.Round(array2[0, 0]), 5] = array[k + 1 + l * (m_Grid_X + 1), 3];
							}
							array2[(int)Math.Round(array2[0, 0]), 5] = array2[(int)Math.Round(array2[0, 0]), 5] + (array[k + l * (m_Grid_X + 1), 3] + array[k + 1 + l * (m_Grid_X + 1), 3] + array[k + (l + 1) * (m_Grid_X + 1), 3] + array[k + 1 + (l + 1) * (m_Grid_X + 1), 3]) / 4f / 2f;
							array2[(int)Math.Round(array2[0, 0]), 1] = k + l * (m_Grid_X + 1);
							array2[(int)Math.Round(array2[0, 0]), 2] = k + (l + 1) * (m_Grid_X + 1);
							array2[(int)Math.Round(array2[0, 0]), 3] = k + 1 + (l + 1) * (m_Grid_X + 1);
							array2[(int)Math.Round(array2[0, 0]), 4] = k + 1 + l * (m_Grid_X + 1);
						}
					}
				}
				do
				{
					l = 0;
					int num37 = (int)Math.Round(array2[0, 0] - 1f);
					for (int k = 1; k <= num37; k++)
					{
						if (array2[k, 0] < array2[k + 1, 0])
						{
							array3[0] = array2[k, 0];
							array3[1] = array2[k, 1];
							array3[2] = array2[k, 2];
							array3[3] = array2[k, 3];
							array3[4] = array2[k, 4];
							array3[5] = array2[k, 5];
							array2[k, 0] = array2[k + 1, 0];
							array2[k, 1] = array2[k + 1, 1];
							array2[k, 2] = array2[k + 1, 2];
							array2[k, 3] = array2[k + 1, 3];
							array2[k, 4] = array2[k + 1, 4];
							array2[k, 5] = array2[k + 1, 5];
							array2[k + 1, 0] = array3[0];
							array2[k + 1, 1] = array3[1];
							array2[k + 1, 2] = array3[2];
							array2[k + 1, 3] = array3[3];
							array2[k + 1, 4] = array3[4];
							array2[k + 1, 5] = array3[5];
							l = 1;
						}
					}
				}
				while (l != 0);
				C_Pen.Color = Color.Black;
				int num38 = (int)Math.Round(array2[0, 0]);
				for (int k = 1; k <= num38; k++)
				{
					l = 0;
					do
					{
						array4[l].X = array[(int)Math.Round(array2[k, l + 1]), 1];
						array4[l].Y = array[(int)Math.Round(array2[k, l + 1]), 2];
						l++;
					}
					while (l <= 3);
					num4 = (int)Math.Round((float)unchecked((int)m_Cell_LowCLR.R) + (float)(m_Cell_HighCLR.R - m_Cell_LowCLR.R) * array2[k, 5]);
					num5 = (int)Math.Round((float)unchecked((int)m_Cell_LowCLR.G) + (float)(m_Cell_HighCLR.G - m_Cell_LowCLR.G) * array2[k, 5]);
					num6 = (int)Math.Round((float)unchecked((int)m_Cell_LowCLR.B) + (float)(m_Cell_HighCLR.B - m_Cell_LowCLR.B) * array2[k, 5]);
					if (num4 < 0)
					{
						num4 = 0;
						if (num5 < 0)
						{
							num5 = 0;
							if (num6 < 0)
							{
								num6 = 0;
							}
						}
					}
					if (num4 > 255)
					{
						num4 = 255;
						if (num5 > 255)
						{
							num5 = 255;
							if (num6 > 255)
							{
								num6 = 255;
							}
						}
					}
					C_Brush.Color = Color.FromArgb(num4, num5, num6);
					val2.FillPolygon((Brush)(object)C_Brush, array4);
					val2.DrawPolygon(C_Pen, array4);
				}
				string text = AutoFormat(GData[GMSX + GMSY * (m_Grid_X + 1)] * m_Grid_DataScalar + m_Grid_DataOffset);
				if (GMMF)
				{
					C_Pen.Color = m_Cell_HSelCLR;
					val2.DrawRectangle(C_Pen, array[GMSX + GMSY * (m_Grid_X + 1), 1] - 3f, array[GMSX + GMSY * (m_Grid_X + 1), 2] - 3f, 6f, 6f);
					C_Pen.Color = Color.Black;
					T_Brush.Color = Color.Black;
					val2.DrawLine(C_Pen, array[GMSX + GMSY * (m_Grid_X + 1), 1] - 5f, array[GMSX + GMSY * (m_Grid_X + 1), 2] - 5f, array[GMSX + GMSY * (m_Grid_X + 1), 1] - 15f, array[GMSX + GMSY * (m_Grid_X + 1), 2] - 15f);
					C_Brush.Color = Color.White;
					val2.FillRectangle((Brush)(object)C_Brush, array[GMSX + GMSY * (m_Grid_X + 1), 1] - 36f, array[GMSX + GMSY * (m_Grid_X + 1), 2] - 31f, (float)(6 + 6 * Strings.Len(text)), 14f);
					val2.DrawRectangle(C_Pen, array[GMSX + GMSY * (m_Grid_X + 1), 1] - 36f, array[GMSX + GMSY * (m_Grid_X + 1), 2] - 31f, (float)(6 + 6 * Strings.Len(text)), 14f);
					val2.DrawString(text, ((Control)this).Font, (Brush)(object)T_Brush, array[GMSX + GMSY * (m_Grid_X + 1), 1] - 35f, array[GMSX + GMSY * (m_Grid_X + 1), 2] - 30f);
				}
				if (m_Grid_ShowLabels == 1)
				{
					text = AutoFormat(GData[GMSX + 0 * (m_Grid_X + 1)]) + " / " + AutoFormat(GData[0 + GMSY * (m_Grid_X + 1)]) + " = " + text;
					val2.DrawString(text, ((Control)this).Font, (Brush)(object)T_Brush, 5f, 5f);
				}
			}
			Graphics val3 = ((Control)Graph).CreateGraphics();
			val3.DrawImageUnscaled((Image)(object)val, 0, 0);
			IsDrawlingG = 0;
		}
	}

	private void Graph_Paint(object sender, PaintEventArgs e)
	{
		Draw_Graph();
	}

	private void Graph_Resize()
	{
		Draw_Graph();
	}

	private void Graph_Closing(object sender, CancelEventArgs e)
	{
		e.Cancel = true;
		((Control)Graph).Hide();
	}

	private void Graph_MouseEnter(object sender, EventArgs e)
	{
		GMMF = true;
	}

	private void Graph_MouseLeave(object sender, EventArgs e)
	{
		GMMF = false;
		Draw_Graph();
	}

	private void Graph_MouseMove(object sender, MouseEventArgs e)
	{
		GMX = e.X;
		GMY = e.Y;
		checked
		{
			if ((GMB == 1) & (Grid_GraphType != 0))
			{
				SData[GMSX + GMSY * (m_Grid_X + 1)] = (byte)(SData[GMSX + GMSY * (m_Grid_X + 1)] | 8);
				GData[GMSX + GMSY * (m_Grid_X + 1)] = GMSV - (float)(GMY - GMCY) * GMSS;
			}
			if ((GMB == 2) & (Grid_GraphType == 2))
			{
				YD = (float)((double)YDS + (double)(GMX - GMCX) / 100.0);
				XD = (float)((double)XDS + (double)(GMY - GMCY) / 100.0 * Math.Cos(YD));
				ZD = (float)((double)ZDS - (double)(GMY - GMCY) / 100.0 * Math.Sin(YD));
			}
			if ((GMB == 3) & (Grid_GraphType == 2))
			{
				VW_X = VW_CX + (float)((GMX - GMCX) * 2);
				VW_Y = VW_CY + (float)((GMY - GMCY) * 2);
			}
			Draw_Graph();
		}
	}

	private void Graph_MouseUp(object sender, MouseEventArgs e)
	{
		if (GMB == 1)
		{
			Draw_Grid();
		}
		GMB = 0;
		GMCX = -1;
		GMCY = -1;
	}

	private void Graph_MouseDown(object sender, MouseEventArgs e)
	{
		//IL_0001: Unknown result type (might be due to invalid IL or missing references)
		//IL_000b: Invalid comparison between Unknown and I4
		//IL_002d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0037: Invalid comparison between Unknown and I4
		if ((int)e.Button == 1048576)
		{
			SaveUndo();
			if (GMB == 2)
			{
				GMB = 3;
			}
			else
			{
				GMB = 1;
			}
		}
		if ((int)e.Button == 2097152)
		{
			if (GMB == 1)
			{
				GMB = 3;
			}
			else
			{
				GMB = 2;
			}
		}
		GMX = e.X;
		GMY = e.Y;
		GMCX = e.X;
		GMCY = e.Y;
		GMSV = GData[checked(GMSX + GMSY * (m_Grid_X + 1))];
		XDS = XD;
		YDS = YD;
		ZDS = ZD;
		VW_CX = VW_X;
		VW_CY = VW_Y;
	}

	private void Graph_MouseWheel(object sender, MouseEventArgs e)
	{
		if (Grid_GraphType == 2)
		{
			VW_ZM = (float)((double)VW_ZM * (1.0 + (double)e.Delta / 1000.0));
			if ((double)VW_ZM < 0.1)
			{
				VW_ZM = 0.1f;
			}
			Draw_Graph();
		}
	}

	private string AutoFormat(float TempF)
	{
		if (TempF > -9f && TempF < 9f)
		{
			return Strings.Format((object)TempF, "0.00");
		}
		if (TempF > -99f && TempF < 99f)
		{
			return Strings.Format((object)TempF, "00.0");
		}
		return Strings.Format((object)TempF, "#####0");
	}

	protected override bool ProcessCmdKey(ref Message msg, Keys keyData)
	{
		//IL_0000: Unknown result type (might be due to invalid IL or missing references)
		//IL_0003: Invalid comparison between Unknown and I4
		//IL_07a6: Unknown result type (might be due to invalid IL or missing references)
		//IL_04e5: Unknown result type (might be due to invalid IL or missing references)
		//IL_04e8: Unknown result type (might be due to invalid IL or missing references)
		//IL_04fe: Expected I4, but got Unknown
		//IL_0226: Unknown result type (might be due to invalid IL or missing references)
		//IL_0229: Unknown result type (might be due to invalid IL or missing references)
		//IL_023f: Expected I4, but got Unknown
		//IL_079d: Unknown result type (might be due to invalid IL or missing references)
		//IL_04de: Unknown result type (might be due to invalid IL or missing references)
		checked
		{
			if (unchecked((int)keyData) == 9)
			{
				if (((Control)TextBox1).Visible)
				{
					((Control)TextBox1).Enabled = false;
					((Control)TextBox1).Visible = false;
					((Control)this).Focus();
					Grid_Math((float)Conversion.Val(TextBox1.Text), 0);
				}
				if (MultiSelect == 0)
				{
					if (m_Grid_Transpose == 0)
					{
						SData[LX + LY * (m_Grid_X + 1)] = (byte)(SData[LX + LY * (m_Grid_X + 1)] & -2);
						LX++;
						if (LX > m_Grid_X)
						{
							LX = 1;
							LY++;
						}
						if (LY > m_Grid_Y)
						{
							LY = m_Grid_Y;
						}
						SData[LX + LY * (m_Grid_X + 1)] = (byte)(SData[LX + LY * (m_Grid_X + 1)] | 1);
					}
					else
					{
						SData[LX + LY * (m_Grid_X + 1)] = (byte)(SData[LX + LY * (m_Grid_X + 1)] & -2);
						LY++;
						if (LY > m_Grid_Y)
						{
							LY = 1;
							LX++;
						}
						if (LX > m_Grid_X)
						{
							LX = m_Grid_X;
						}
						SData[LX + LY * (m_Grid_X + 1)] = (byte)(SData[LX + LY * (m_Grid_X + 1)] | 1);
					}
				}
				Draw_Grid();
				return true;
			}
			if ((MultiSelect == 0) & !((Control)TextBox1).Visible)
			{
				if (m_Grid_Transpose == 0)
				{
					switch (unchecked(keyData - 37))
					{
					case 0:
						SData[LX + LY * (m_Grid_X + 1)] = (byte)(SData[LX + LY * (m_Grid_X + 1)] & -2);
						LX--;
						if (LX < 1)
						{
							LX = 1;
						}
						SData[LX + LY * (m_Grid_X + 1)] = (byte)(SData[LX + LY * (m_Grid_X + 1)] | 1);
						Draw_Grid();
						return true;
					case 2:
						SData[LX + LY * (m_Grid_X + 1)] = (byte)(SData[LX + LY * (m_Grid_X + 1)] & -2);
						LX++;
						if (LX > m_Grid_X)
						{
							LX = m_Grid_X;
						}
						SData[LX + LY * (m_Grid_X + 1)] = (byte)(SData[LX + LY * (m_Grid_X + 1)] | 1);
						Draw_Grid();
						return true;
					case 1:
						SData[LX + LY * (m_Grid_X + 1)] = (byte)(SData[LX + LY * (m_Grid_X + 1)] & -2);
						LY--;
						if (LY < 1)
						{
							LY = 1;
						}
						SData[LX + LY * (m_Grid_X + 1)] = (byte)(SData[LX + LY * (m_Grid_X + 1)] | 1);
						Draw_Grid();
						return true;
					case 3:
						SData[LX + LY * (m_Grid_X + 1)] = (byte)(SData[LX + LY * (m_Grid_X + 1)] & -2);
						LY++;
						if (LY > m_Grid_Y)
						{
							LY = m_Grid_Y;
						}
						SData[LX + LY * (m_Grid_X + 1)] = (byte)(SData[LX + LY * (m_Grid_X + 1)] | 1);
						Draw_Grid();
						return true;
					default:
						return ((ContainerControl)this).ProcessCmdKey(ref msg, keyData);
					}
				}
				switch (unchecked(keyData - 37))
				{
				case 1:
					SData[LX + LY * (m_Grid_X + 1)] = (byte)(SData[LX + LY * (m_Grid_X + 1)] & -2);
					LX--;
					if (LX < 1)
					{
						LX = 1;
					}
					SData[LX + LY * (m_Grid_X + 1)] = (byte)(SData[LX + LY * (m_Grid_X + 1)] | 1);
					Draw_Grid();
					return true;
				case 3:
					SData[LX + LY * (m_Grid_X + 1)] = (byte)(SData[LX + LY * (m_Grid_X + 1)] & -2);
					LX++;
					if (LX > m_Grid_X)
					{
						LX = m_Grid_X;
					}
					SData[LX + LY * (m_Grid_X + 1)] = (byte)(SData[LX + LY * (m_Grid_X + 1)] | 1);
					Draw_Grid();
					return true;
				case 0:
					SData[LX + LY * (m_Grid_X + 1)] = (byte)(SData[LX + LY * (m_Grid_X + 1)] & -2);
					LY--;
					if (LY < 1)
					{
						LY = 1;
					}
					SData[LX + LY * (m_Grid_X + 1)] = (byte)(SData[LX + LY * (m_Grid_X + 1)] | 1);
					Draw_Grid();
					return true;
				case 2:
					SData[LX + LY * (m_Grid_X + 1)] = (byte)(SData[LX + LY * (m_Grid_X + 1)] & -2);
					LY++;
					if (LY > m_Grid_Y)
					{
						LY = m_Grid_Y;
					}
					SData[LX + LY * (m_Grid_X + 1)] = (byte)(SData[LX + LY * (m_Grid_X + 1)] | 1);
					Draw_Grid();
					return true;
				default:
					return ((ContainerControl)this).ProcessCmdKey(ref msg, keyData);
				}
			}
			return ((ContainerControl)this).ProcessCmdKey(ref msg, keyData);
		}
	}

	private void Control_KeyDown(object sender, KeyEventArgs e)
	{
		//IL_0010: Unknown result type (might be due to invalid IL or missing references)
		//IL_0017: Invalid comparison between Unknown and I4
		if (e.Control)
		{
			ControlButton = 1;
		}
		if ((int)e.KeyCode != 46)
		{
			return;
		}
		SaveUndo();
		int grid_X = m_Grid_X;
		checked
		{
			for (int i = 1; i <= grid_X; i++)
			{
				int grid_Y = m_Grid_Y;
				for (int j = 1; j <= grid_Y; j++)
				{
					if ((SData[i + j * (m_Grid_X + 1)] & 1) != 0)
					{
						SData[i + j * (m_Grid_X + 1)] = (byte)(SData[i + j * (m_Grid_X + 1)] | 8);
						GData[i + j * (m_Grid_X + 1)] = 100000000f;
					}
				}
			}
			Draw_Grid();
		}
	}

	private void Control_KeyUp(object sender, KeyEventArgs e)
	{
		if (!e.Control)
		{
			ControlButton = 0;
		}
	}

	private void Control_KeyPress(object sender, KeyPressEventArgs e)
	{
		checked
		{
			if ((Strings.Asc(e.KeyChar) >= 45) & (Strings.Asc(e.KeyChar) < 58) & !((Control)TextBox1).Visible)
			{
				Point location = default(Point);
				if (m_Grid_Transpose == 0)
				{
					location.X = (LX - 1 + m_Grid_ShowLabels) * m_Cell_W;
					location.Y = (LY - 1 + m_Grid_ShowLabels) * m_Cell_H;
				}
				else
				{
					location.X = (LY - 1 + m_Grid_ShowLabels) * m_Cell_W;
					location.Y = (LX - 1 + m_Grid_ShowLabels) * m_Cell_H;
				}
				((Control)TextBox1).Location = location;
				((Control)TextBox1).Enabled = true;
				((Control)TextBox1).Visible = true;
				((Control)TextBox1).Focus();
				TextBox1.Text = "";
				((TextBoxBase)TextBox1).DeselectAll();
				((TextBoxBase)TextBox1).AppendText(Conversions.ToString(e.KeyChar));
			}
		}
	}

	private void TextBox1_KeyPress(object sender, KeyPressEventArgs e)
	{
		if (e.KeyChar == '\r')
		{
			((Control)TextBox1).Enabled = false;
			((Control)TextBox1).Visible = false;
			((Control)this).Focus();
			e.Handled = true;
			Grid_Math((float)Conversion.Val(TextBox1.Text), 0);
			Draw_Grid();
		}
		else if (e.KeyChar == '\u001b')
		{
			TextBox1.Text = "";
			((Control)TextBox1).Enabled = false;
			((Control)TextBox1).Visible = false;
			((Control)this).Focus();
			e.Handled = true;
			Draw_Grid();
		}
	}

	private void TextBox1_LostFocus(object sender, EventArgs e)
	{
		((Control)TextBox1).Enabled = false;
		((Control)TextBox1).Visible = false;
	}

	private void Control_MouseMove(object sender, MouseEventArgs e)
	{
		if (!((L2X != -1) | (L2Y != -1)))
		{
			return;
		}
		checked
		{
			int num;
			int num2;
			if (m_Grid_Transpose == 0)
			{
				num = (int)Math.Round(Conversion.Int((double)e.X / (double)m_Cell_W - (double)unchecked((int)m_Grid_ShowLabels)) + 1.0);
				num2 = (int)Math.Round(Conversion.Int((double)e.Y / (double)m_Cell_H - (double)unchecked((int)m_Grid_ShowLabels)) + 1.0);
			}
			else
			{
				num2 = (int)Math.Round(Conversion.Int((double)e.X / (double)m_Cell_W - (double)unchecked((int)m_Grid_ShowLabels)) + 1.0);
				num = (int)Math.Round(Conversion.Int((double)e.Y / (double)m_Cell_H - (double)unchecked((int)m_Grid_ShowLabels)) + 1.0);
			}
			if (!((num != L2X) | (num2 != L2Y)))
			{
				return;
			}
			int grid_X = m_Grid_X;
			for (int i = 1; i <= grid_X; i++)
			{
				int grid_Y = m_Grid_Y;
				for (int j = 1; j <= grid_Y; j++)
				{
					SData[i + j * (m_Grid_X + 1)] = (byte)(SData[i + j * (m_Grid_X + 1)] & -3);
				}
			}
			if (!((num == LX) & (num2 == LY)))
			{
				int num3 = 999;
				if (num < num3)
				{
					num3 = num;
				}
				if (LX < num3)
				{
					num3 = LX;
				}
				int num4 = 0;
				if (num > num4)
				{
					num4 = num;
				}
				if (LX > num4)
				{
					num4 = LX;
				}
				int num5 = 999;
				if (num2 < num5)
				{
					num5 = num2;
				}
				if (LY < num5)
				{
					num5 = LY;
				}
				int num6 = 0;
				if (num2 > num6)
				{
					num6 = num2;
				}
				if (LY > num6)
				{
					num6 = LY;
				}
				if (LX == 0)
				{
					num3 = 1;
					num4 = m_Grid_X;
				}
				if (LY == 0)
				{
					num5 = 1;
					num6 = m_Grid_Y;
				}
				if (num3 < 1)
				{
					num3 = 1;
				}
				if (num4 > m_Grid_X)
				{
					num4 = m_Grid_X;
				}
				if (num5 < 1)
				{
					num5 = 1;
				}
				if (num6 > m_Grid_Y)
				{
					num6 = m_Grid_Y;
				}
				int num7 = num3;
				int num8 = num4;
				for (int i = num7; i <= num8; i++)
				{
					int num9 = num5;
					int num10 = num6;
					for (int j = num9; j <= num10; j++)
					{
						SData[i + j * (m_Grid_X + 1)] = (byte)(SData[i + j * (m_Grid_X + 1)] | 2);
					}
				}
				Draw_Grid();
			}
			L2X = num;
			L2Y = num2;
		}
	}

	private void Contorl_MouseLeave(object sender, EventArgs e)
	{
		Check_Select();
		Draw_Grid();
	}

	private void Contorl_MouseDown(object sender, MouseEventArgs e)
	{
		//IL_0026: Unknown result type (might be due to invalid IL or missing references)
		//IL_0030: Invalid comparison between Unknown and I4
		int num = 0;
		int num2 = 0;
		if (((Computer)MyProject.Computer).Keyboard.CtrlKeyDown)
		{
			ControlButton = 1;
		}
		else
		{
			ControlButton = 0;
		}
		if ((int)e.Button == 1048576)
		{
			num = 1;
		}
		num2 = ((ControlButton == 1) ? 2 : 0);
		if (((Operators.CompareString(TextBox1.Text, "", false) != 0) & ((Control)TextBox1).Enabled) && num == 1)
		{
			Grid_Math((float)Conversion.Val(TextBox1.Text), 0);
		}
		MouseGrid(num, num2, e.X, e.Y, 1);
		((Control)TextBox1).Enabled = false;
		((Control)TextBox1).Visible = false;
		((Control)this).Focus();
		Draw_Grid();
	}

	private void Control_MouseUp(object sender, MouseEventArgs e)
	{
		//IL_0005: Unknown result type (might be due to invalid IL or missing references)
		//IL_000f: Invalid comparison between Unknown and I4
		int button = 0;
		int num = 0;
		if ((int)e.Button == 1048576)
		{
			button = 1;
		}
		num = ((ControlButton == 1) ? 2 : 0);
		MouseGrid(button, num, e.X, e.Y, 0);
		Draw_Grid();
	}

	private void MouseGrid(int Button, int Shift, int X, int Y, byte D)
	{
		int num;
		int num2;
		checked
		{
			if (m_Grid_Transpose == 0)
			{
				num = (int)Math.Round(Conversion.Int((double)X / (double)m_Cell_W - (double)unchecked((int)m_Grid_ShowLabels)) + 1.0);
				num2 = (int)Math.Round(Conversion.Int((double)Y / (double)m_Cell_H - (double)unchecked((int)m_Grid_ShowLabels)) + 1.0);
			}
			else
			{
				num2 = (int)Math.Round(Conversion.Int((double)X / (double)m_Cell_W - (double)unchecked((int)m_Grid_ShowLabels)) + 1.0);
				num = (int)Math.Round(Conversion.Int((double)Y / (double)m_Cell_H - (double)unchecked((int)m_Grid_ShowLabels)) + 1.0);
			}
		}
		if (Button == 1 && D == 1)
		{
			if ((((num >= 0) & (num <= m_Grid_X)) && num2 >= 0) & (num2 <= m_Grid_Y))
			{
				checked
				{
					if (Shift != 2)
					{
						int grid_X = m_Grid_X;
						for (int i = 1; i <= grid_X; i++)
						{
							int grid_Y = m_Grid_Y;
							for (int j = 1; j <= grid_Y; j++)
							{
								SData[i + j * (m_Grid_X + 1)] = (byte)(SData[i + j * (m_Grid_X + 1)] & -4);
							}
						}
					}
					int num3;
					int num4;
					if (num == 0)
					{
						num3 = 1;
						num4 = m_Grid_X;
					}
					else
					{
						num3 = num;
						num4 = num;
					}
					int num5;
					int num6;
					if (num2 == 0)
					{
						num5 = 1;
						num6 = m_Grid_Y;
					}
					else
					{
						num5 = num2;
						num6 = num2;
					}
					int num7 = num3;
					int num8 = num4;
					for (int i = num7; i <= num8; i++)
					{
						int num9 = num5;
						int num10 = num6;
						for (int j = num9; j <= num10; j++)
						{
							if (unchecked(Shift == 2 && num != 0 && num2 != 0))
							{
								SData[i + j * (m_Grid_X + 1)] = (byte)(SData[i + j * (m_Grid_X + 1)] ^ 1);
							}
							else
							{
								SData[i + j * (m_Grid_X + 1)] = (byte)(SData[i + j * (m_Grid_X + 1)] | 1);
							}
						}
					}
					LX = num;
					LY = num2;
					L2X = num;
					L2Y = num2;
				}
			}
			else
			{
				Check_Select();
			}
		}
		if (!(Button == 1 && D == 0) || !((((num >= 0) & (num <= m_Grid_X)) && num2 >= 0) & (num2 <= m_Grid_Y)))
		{
			return;
		}
		int grid_X2 = m_Grid_X;
		checked
		{
			for (int i = 1; i <= grid_X2; i++)
			{
				int grid_Y2 = m_Grid_Y;
				for (int j = 1; j <= grid_Y2; j++)
				{
					SData[i + j * (m_Grid_X + 1)] = (byte)(SData[i + j * (m_Grid_X + 1)] & -3);
				}
			}
			if (!((num == LX) & (num2 == LY)))
			{
				int num3 = 999;
				if (num < num3)
				{
					num3 = num;
				}
				if (LX < num3)
				{
					num3 = LX;
				}
				int num4 = 0;
				if (num > num4)
				{
					num4 = num;
				}
				if (LX > num4)
				{
					num4 = LX;
				}
				int num5 = 999;
				if (num2 < num5)
				{
					num5 = num2;
				}
				if (LY < num5)
				{
					num5 = LY;
				}
				int num6 = 0;
				if (num2 > num6)
				{
					num6 = num2;
				}
				if (LY > num6)
				{
					num6 = LY;
				}
				if (LX == 0)
				{
					num3 = 1;
					num4 = m_Grid_X;
				}
				if (LY == 0)
				{
					num5 = 1;
					num6 = m_Grid_Y;
				}
				if (num3 < 1)
				{
					num3 = 1;
				}
				if (num4 > m_Grid_X)
				{
					num4 = m_Grid_X;
				}
				if (num5 < 1)
				{
					num5 = 1;
				}
				if (num6 > m_Grid_Y)
				{
					num6 = m_Grid_Y;
				}
				int num11 = num3;
				int num12 = num4;
				for (int i = num11; i <= num12; i++)
				{
					int num13 = num5;
					int num14 = num6;
					for (int j = num13; j <= num14; j++)
					{
						SData[i + j * (m_Grid_X + 1)] = (byte)(SData[i + j * (m_Grid_X + 1)] | 1);
					}
				}
			}
			Check_Select();
		}
	}

	private void Check_Select()
	{
		int num = 9999;
		int num2 = 9999;
		L2X = -1;
		L2Y = -1;
		if (LX < 1)
		{
			LX = 1;
		}
		if (LX > m_Grid_X)
		{
			LX = m_Grid_X;
		}
		if (LY < 1)
		{
			LY = 1;
		}
		if (LY > m_Grid_Y)
		{
			LY = m_Grid_Y;
		}
		MultiSelect = -1;
		int grid_X = m_Grid_X;
		checked
		{
			for (int i = 1; i <= grid_X; i++)
			{
				int grid_Y = m_Grid_Y;
				for (int j = 1; j <= grid_Y; j++)
				{
					if (((SData[i + j * (m_Grid_X + 1)] & 1) | (SData[i + j * (m_Grid_X + 1)] & 2)) != 0)
					{
						if (i < num)
						{
							num = i;
						}
						if (j < num2)
						{
							num2 = j;
						}
						SData[i + j * (m_Grid_X + 1)] = (byte)(SData[i + j * (m_Grid_X + 1)] & -3);
						SData[i + j * (m_Grid_X + 1)] = (byte)(SData[i + j * (m_Grid_X + 1)] | 1);
						MultiSelect++;
					}
				}
			}
			if (MultiSelect < 0)
			{
				MultiSelect = -1;
				LX = 1;
				LY = 1;
			}
			if (MultiSelect == 0)
			{
				MultiSelect = 0;
				LX = num;
				LY = num2;
			}
			if (MultiSelect >= 1)
			{
				MultiSelect = 1;
				LX = num;
				LY = num2;
			}
		}
	}

	private void EditToolStripMenuItem_Click(object sender, EventArgs e)
	{
	}

	private void FillToolStripMenuItem_Click(object sender, EventArgs e)
	{
		Grid_Math((float)Conversion.Val(((ToolStripControlHost)ToolStripTextBox1).Text), 0);
		Draw_Grid();
		((Control)DataMenuStrip).Hide();
	}

	private void AddToolStripMenuItem_Click(object sender, EventArgs e)
	{
		Grid_Math((float)Conversion.Val(((ToolStripControlHost)ToolStripTextBox1).Text), 1);
		Draw_Grid();
		((Control)DataMenuStrip).Hide();
	}

	private void SubtractToolStripMenuItem_Click(object sender, EventArgs e)
	{
		Grid_Math((float)Conversion.Val(((ToolStripControlHost)ToolStripTextBox1).Text), 2);
		Draw_Grid();
		((Control)DataMenuStrip).Hide();
	}

	private void MultiplyToolStripMenuItem_Click(object sender, EventArgs e)
	{
		Grid_Math((float)Conversion.Val(((ToolStripControlHost)ToolStripTextBox1).Text), 3);
		Draw_Grid();
		((Control)DataMenuStrip).Hide();
	}

	private void DivideToolStripMenuItem_Click(object sender, EventArgs e)
	{
		Grid_Math((float)Conversion.Val(((ToolStripControlHost)ToolStripTextBox1).Text), 4);
		Draw_Grid();
		((Control)DataMenuStrip).Hide();
	}

	private void CopyToolStripMenuItem_Click(object sender, EventArgs e)
	{
		CopyClipboard(0);
		((Control)DataMenuStrip).Hide();
	}

	private void CopyLabelsToolStripMenuItem_Click(object sender, EventArgs e)
	{
		CopyClipboard(1);
		((Control)DataMenuStrip).Hide();
	}

	private void PasteToolStripMenuItem_Click(object sender, EventArgs e)
	{
		PasteClipboard(0);
		((Control)DataMenuStrip).Hide();
	}

	private void PasteLabelsToolStripMenuItem_Click(object sender, EventArgs e)
	{
		PasteClipboard(1);
		((Control)DataMenuStrip).Hide();
	}

	private void PasteLabelsInterpolateToolStripMenuItem_Click(object sender, EventArgs e)
	{
		PasteClipboard(2);
		((Control)DataMenuStrip).Hide();
	}

	private void PasteAddToolStripMenuItem_Click(object sender, EventArgs e)
	{
		PasteClipboard(3);
		((Control)DataMenuStrip).Hide();
	}

	private void PasteSubtractToolStripMenuItem_Click(object sender, EventArgs e)
	{
		PasteClipboard(4);
		((Control)DataMenuStrip).Hide();
	}

	private void PasteMultiplyToolStripMenuItem_Click(object sender, EventArgs e)
	{
		PasteClipboard(5);
		((Control)DataMenuStrip).Hide();
	}

	private void PasteMultiplyPctToolStripMenuItem_Click(object sender, EventArgs e)
	{
		PasteClipboard(6);
		((Control)DataMenuStrip).Hide();
	}

	private void PasteMultiplyPctHalfToolStripMenuItem_Click(object sender, EventArgs e)
	{
		PasteClipboard(7);
		((Control)DataMenuStrip).Hide();
	}

	private void PasteDivideToolStripMenuItem_Click(object sender, EventArgs e)
	{
		PasteClipboard(8);
		((Control)DataMenuStrip).Hide();
	}

	private void PasteAverageToolStripMenuItem_Click(object sender, EventArgs e)
	{
		PasteClipboard(9);
		((Control)DataMenuStrip).Hide();
	}

	private void ManipulateToolStripMenuItem_Click(object sender, EventArgs e)
	{
	}

	private void SmoothToolStripMenuItem_Click(object sender, EventArgs e)
	{
		Smooth(0);
		Draw_Grid();
		((Control)DataMenuStrip).Hide();
	}

	private void SmoothHorizontalToolStripMenuItem_Click(object sender, EventArgs e)
	{
		if (m_Grid_Transpose == 1)
		{
			Smooth(2);
		}
		else
		{
			Smooth(1);
		}
		Draw_Grid();
		((Control)DataMenuStrip).Hide();
	}

	private void SmoothVerticalToolStripMenuItem_Click(object sender, EventArgs e)
	{
		if (m_Grid_Transpose == 1)
		{
			Smooth(1);
		}
		else
		{
			Smooth(2);
		}
		Draw_Grid();
		((Control)DataMenuStrip).Hide();
	}

	private void InterpolateToolStripMenuItem_Click(object sender, EventArgs e)
	{
		Interpolate(0);
		Draw_Grid();
		((Control)DataMenuStrip).Hide();
	}

	private void InterpolateHorizontalToolStripMenuItem_Click(object sender, EventArgs e)
	{
		if (m_Grid_Transpose == 1)
		{
			Interpolate(2);
		}
		else
		{
			Interpolate(1);
		}
		Draw_Grid();
		((Control)DataMenuStrip).Hide();
	}

	private void InterpolateVerticalToolStripMenuItem_Click(object sender, EventArgs e)
	{
		if (m_Grid_Transpose == 1)
		{
			Interpolate(1);
		}
		else
		{
			Interpolate(2);
		}
		Draw_Grid();
		((Control)DataMenuStrip).Hide();
	}

	private void ExtrapolateToolStripMenuItem_Click(object sender, EventArgs e)
	{
		Extrapolate();
		Draw_Grid();
		((Control)DataMenuStrip).Hide();
	}

	private void SelectNullsToolStripMenuItem_Click(object sender, EventArgs e)
	{
		Select_Null();
		((Control)DataMenuStrip).Hide();
	}

	private void SelectNonNullsToolStripMenuItem_Click(object sender, EventArgs e)
	{
		Select_NonNull();
		((Control)DataMenuStrip).Hide();
	}

	private void SelectZerosToolStripMenuItem_Click(object sender, EventArgs e)
	{
		Select_Zero();
		((Control)DataMenuStrip).Hide();
	}

	private void SelectNonZerosToolStripMenuItem_Click(object sender, EventArgs e)
	{
		Select_NonZero();
		((Control)DataMenuStrip).Hide();
	}

	private void SelectPositiveToolStripMenuItem_Click(object sender, EventArgs e)
	{
		Select_Positive();
		((Control)DataMenuStrip).Hide();
	}

	private void SelectNegativeToolStripMenuItem_Click(object sender, EventArgs e)
	{
		Select_Negative();
		((Control)DataMenuStrip).Hide();
	}

	private void TransposeClipboardToolStripMenuItem_Click(object sender, EventArgs e)
	{
		TransposeClipboard();
		((Control)DataMenuStrip).Hide();
	}

	private void ScaleXAxisMenuItem_Click(object sender, EventArgs e)
	{
		X_Scale_Clipboard((float)Conversion.Val(((ToolStripControlHost)ToolStripTextBox2).Text));
	}

	private void ScaleYAxisMenuItem_Click(object sender, EventArgs e)
	{
		Y_Scale_Clipboard((float)Conversion.Val(((ToolStripControlHost)ToolStripTextBox2).Text));
	}

	private void ImportAxisMenuItem_Click(object sender, EventArgs e)
	{
		Import_Axes_Clipboard();
	}

	private void ClearChangedFlagToolStripMenuItem_Click(object sender, EventArgs e)
	{
		Clear_Changed_Flags();
		Draw_Grid();
		((Control)DataMenuStrip).Hide();
	}

	private void ToggleChangeFlagDisplayToolStripMenuItem_Click(object sender, EventArgs e)
	{
		if (m_Cell_ShowChanges == 0)
		{
			m_Cell_ShowChanges = 1;
		}
		else
		{
			m_Cell_ShowChanges = 0;
		}
		Draw_Grid();
		((Control)DataMenuStrip).Hide();
	}

	private void ClearTableToZerosToolStripMenuItem_Click(object sender, EventArgs e)
	{
		Clear_to_Zero();
	}

	private void ClearTableToNullsToolStripMenuItem_Click(object sender, EventArgs e)
	{
		Clear_to_Null();
	}

	private void ConvertZerosToNullsToolStripMenuItem_Click(object sender, EventArgs e)
	{
		Zero_to_Null();
	}

	private void ConvertNullsToZerosToolStripMenuItem_Click(object sender, EventArgs e)
	{
		Null_to_Zero();
	}

	private void GraphToolStripMenuItem_Click(object sender, EventArgs e)
	{
	}

	private void Graph2DToolStripMenuItem_Click(object sender, EventArgs e)
	{
		m_Grid_GraphType = 1;
		((Control)Graph).Show();
		Draw_Graph();
		((Control)DataMenuStrip).Hide();
	}

	private void Graph3DToolStripMenuItem_Click(object sender, EventArgs e)
	{
		m_Grid_GraphType = 2;
		((Control)Graph).Show();
		Draw_Graph();
		((Control)DataMenuStrip).Hide();
	}

	public void Select_All()
	{
		int grid_X = m_Grid_X;
		checked
		{
			for (int i = 1; i <= grid_X; i++)
			{
				int grid_Y = m_Grid_Y;
				for (int j = 1; j <= grid_Y; j++)
				{
					SData[i + j * (m_Grid_X + 1)] = (byte)(SData[i + j * (m_Grid_X + 1)] | 1);
				}
			}
			Check_Select();
			Draw_Grid();
		}
	}

	public void Select_Null()
	{
		if (ControlButton == 0)
		{
			Clear_Selected();
		}
		int grid_X = m_Grid_X;
		checked
		{
			for (int i = 1; i <= grid_X; i++)
			{
				int grid_Y = m_Grid_Y;
				for (int j = 1; j <= grid_Y; j++)
				{
					if (GData[i + j * (m_Grid_X + 1)] >= 100000000f)
					{
						SData[i + j * (m_Grid_X + 1)] = (byte)(SData[i + j * (m_Grid_X + 1)] | 1);
					}
				}
			}
			Draw_Grid();
		}
	}

	public void Select_NonNull()
	{
		if (ControlButton == 0)
		{
			Clear_Selected();
		}
		int grid_X = m_Grid_X;
		checked
		{
			for (int i = 1; i <= grid_X; i++)
			{
				int grid_Y = m_Grid_Y;
				for (int j = 1; j <= grid_Y; j++)
				{
					if (GData[i + j * (m_Grid_X + 1)] < 100000000f)
					{
						SData[i + j * (m_Grid_X + 1)] = (byte)(SData[i + j * (m_Grid_X + 1)] | 1);
					}
				}
			}
			Draw_Grid();
		}
	}

	public void Select_Zero()
	{
		if (ControlButton == 0)
		{
			Clear_Selected();
		}
		int grid_X = m_Grid_X;
		checked
		{
			for (int i = 1; i <= grid_X; i++)
			{
				int grid_Y = m_Grid_Y;
				for (int j = 1; j <= grid_Y; j++)
				{
					if (GData[i + j * (m_Grid_X + 1)] == 0f)
					{
						SData[i + j * (m_Grid_X + 1)] = (byte)(SData[i + j * (m_Grid_X + 1)] | 1);
					}
				}
			}
			Draw_Grid();
		}
	}

	public void Select_NonZero()
	{
		if (ControlButton == 0)
		{
			Clear_Selected();
		}
		int grid_X = m_Grid_X;
		checked
		{
			for (int i = 1; i <= grid_X; i++)
			{
				int grid_Y = m_Grid_Y;
				for (int j = 1; j <= grid_Y; j++)
				{
					if ((GData[i + j * (m_Grid_X + 1)] != 0f) & (GData[i + j * (m_Grid_X + 1)] < 100000000f))
					{
						SData[i + j * (m_Grid_X + 1)] = (byte)(SData[i + j * (m_Grid_X + 1)] | 1);
					}
				}
			}
			Draw_Grid();
		}
	}

	public void Select_Negative()
	{
		if (ControlButton == 0)
		{
			Clear_Selected();
		}
		int grid_X = m_Grid_X;
		checked
		{
			for (int i = 1; i <= grid_X; i++)
			{
				int grid_Y = m_Grid_Y;
				for (int j = 1; j <= grid_Y; j++)
				{
					if (GData[i + j * (m_Grid_X + 1)] < 0f)
					{
						SData[i + j * (m_Grid_X + 1)] = (byte)(SData[i + j * (m_Grid_X + 1)] | 1);
					}
				}
			}
			Draw_Grid();
		}
	}

	public void Select_Positive()
	{
		if (ControlButton == 0)
		{
			Clear_Selected();
		}
		int grid_X = m_Grid_X;
		checked
		{
			for (int i = 1; i <= grid_X; i++)
			{
				int grid_Y = m_Grid_Y;
				for (int j = 1; j <= grid_Y; j++)
				{
					if ((GData[i + j * (m_Grid_X + 1)] > 0f) & (GData[i + j * (m_Grid_X + 1)] < 100000000f))
					{
						SData[i + j * (m_Grid_X + 1)] = (byte)(SData[i + j * (m_Grid_X + 1)] | 1);
					}
				}
			}
			Draw_Grid();
		}
	}

	public void Clear_Selected()
	{
		int grid_X = m_Grid_X;
		checked
		{
			for (int i = 1; i <= grid_X; i++)
			{
				int grid_Y = m_Grid_Y;
				for (int j = 1; j <= grid_Y; j++)
				{
					SData[i + j * (m_Grid_X + 1)] = (byte)(SData[i + j * (m_Grid_X + 1)] & -4);
				}
			}
			Check_Select();
			Draw_Grid();
		}
	}

	private void Clear_Changed_Flags()
	{
		int grid_X = m_Grid_X;
		checked
		{
			for (int i = 1; i <= grid_X; i++)
			{
				int grid_Y = m_Grid_Y;
				for (int j = 1; j <= grid_Y; j++)
				{
					SData[i + j * (m_Grid_X + 1)] = (byte)(SData[i + j * (m_Grid_X + 1)] & -9);
				}
			}
		}
	}

	public void Clear_to_Null()
	{
		SaveUndo();
		int grid_X = m_Grid_X;
		checked
		{
			for (int i = 1; i <= grid_X; i++)
			{
				int grid_Y = m_Grid_Y;
				for (int j = 1; j <= grid_Y; j++)
				{
					GData[i + j * (m_Grid_X + 1)] = 100000000f;
				}
			}
			Draw_Grid();
		}
	}

	public void Clear_to_Zero()
	{
		SaveUndo();
		int grid_X = m_Grid_X;
		checked
		{
			for (int i = 1; i <= grid_X; i++)
			{
				int grid_Y = m_Grid_Y;
				for (int j = 1; j <= grid_Y; j++)
				{
					GData[i + j * (m_Grid_X + 1)] = 0f;
				}
			}
			Draw_Grid();
		}
	}

	public void Null_to_Zero()
	{
		SaveUndo();
		int grid_X = m_Grid_X;
		checked
		{
			for (int i = 1; i <= grid_X; i++)
			{
				int grid_Y = m_Grid_Y;
				for (int j = 1; j <= grid_Y; j++)
				{
					if (GData[i + j * (m_Grid_X + 1)] >= 100000000f)
					{
						GData[i + j * (m_Grid_X + 1)] = 0f;
					}
				}
			}
			Draw_Grid();
		}
	}

	public void Zero_to_Null()
	{
		SaveUndo();
		int grid_X = m_Grid_X;
		checked
		{
			for (int i = 1; i <= grid_X; i++)
			{
				int grid_Y = m_Grid_Y;
				for (int j = 1; j <= grid_Y; j++)
				{
					if (GData[i + j * (m_Grid_X + 1)] == 0f)
					{
						GData[i + j * (m_Grid_X + 1)] = 100000000f;
					}
				}
			}
			Draw_Grid();
		}
	}

	public void CopyClipboard(int F)
	{
		string text = "";
		int num = MAX_X;
		int num2 = 0;
		int num3 = MAX_Y;
		int num4 = 0;
		int num5 = 1;
		int grid_X = m_Grid_X;
		checked
		{
			for (int i = 1; i <= grid_X; i++)
			{
				int grid_Y = m_Grid_Y;
				for (int j = 1; j <= grid_Y; j++)
				{
					if ((SData[i + j * (m_Grid_X + 1)] & 1) != 0)
					{
						num5 = 0;
						if (i < num)
						{
							num = i;
						}
						if (i > num2)
						{
							num2 = i;
						}
						if (j < num3)
						{
							num3 = j;
						}
						if (j > num4)
						{
							num4 = j;
						}
					}
				}
			}
			if (num5 == 1)
			{
				num = 1;
				num2 = m_Grid_X;
				num3 = 1;
				num4 = m_Grid_Y;
			}
			if (F == 1)
			{
				text += "Labels";
				text += "\t";
				int num6 = num;
				int num7 = num2;
				for (int i = num6; i <= num7; i++)
				{
					float num8 = GData[i + 0 * (m_Grid_X + 1)];
					text += Strings.Format((object)num8, m_Cell_CPFormat);
					if (i != num2)
					{
						text += "\t";
					}
				}
				text += "\r\n";
			}
			int num9 = num3;
			int num10 = num4;
			for (int j = num9; j <= num10; j++)
			{
				if (F == 1)
				{
					float num8 = GData[0 + j * (m_Grid_X + 1)];
					text += Strings.Format((object)num8, m_Cell_CPFormat);
					text += "\t";
				}
				int num11 = num;
				int num12 = num2;
				for (int i = num11; i <= num12; i++)
				{
					float num8 = GData[i + j * (m_Grid_X + 1)];
					unchecked
					{
						if (((0 - ((num8 < 100000000f) ? 1 : 0)) & ((SData[checked(i + j * (m_Grid_X + 1))] & 1) | (0 - ((num5 == 1) ? 1 : 0)))) != 0)
						{
							text = ((m_Grid_DataSCopyPaste != 1) ? (text + Strings.Format((object)num8, m_Cell_CPFormat)) : (text + Strings.Format((object)(num8 * m_Grid_DataScalar + m_Grid_DataOffset), m_Cell_CPFormat)));
						}
						if (!(j == num4 && i == num2))
						{
							text = ((i != num2) ? (text + "\t") : (text + "\r\n"));
						}
					}
				}
			}
			Clipboard.Clear();
			Clipboard.SetText(text);
			if (m_Grid_TransposeCopyPaste == 1)
			{
				TransposeClipboard();
			}
			((Control)DataMenuStrip).Hide();
			((Control)this).Focus();
		}
	}

	public void PasteClipboard(int F)
	{
		SaveUndo();
		string text = "";
		string text2 = "";
		string text3 = "";
		string text4 = "";
		int num = 1;
		int num2 = 1;
		long num3 = 1L;
		byte b = 0;
		text = Clipboard.GetText();
		text2 = text;
		if (m_Grid_TransposeCopyPaste == 1)
		{
			TransposeClipboard();
			text = Clipboard.GetText();
		}
		if (F == 1 || F == 2)
		{
			PastewLabels(F);
		}
		else
		{
			num = LX;
			num2 = LY;
			text3 = "";
			long num4 = 1L;
			long num5 = Strings.Len(text);
			checked
			{
				for (num3 = num4; num3 <= num5; num3++)
				{
					text4 = Strings.Mid(text, (int)num3, 1);
					switch (text4)
					{
					case "\t":
						if ((num <= m_Grid_X) & (num2 <= m_Grid_Y))
						{
							if (Operators.CompareString(text3, "Labels", false) == 0)
							{
								b = 1;
							}
							if (unchecked(Operators.CompareString(text3, "", false) != 0 && b != 1))
							{
								PasteF(F, (float)Conversion.Val(text3), num, num2);
							}
						}
						text3 = "";
						if (b != 2)
						{
							num++;
						}
						if (b == 2)
						{
							b = 3;
						}
						break;
					case "\r":
						if (unchecked(((num <= m_Grid_X) & (num2 <= m_Grid_Y)) && Operators.CompareString(text3, "", false) != 0 && b != 1))
						{
							PasteF(F, (float)Conversion.Val(text3), num, num2);
						}
						text3 = "";
						num = LX;
						if (b != 1)
						{
							num2++;
						}
						if (b == 1)
						{
							b = 2;
						}
						if (b == 3)
						{
							b = 2;
						}
						break;
					default:
						text3 += text4;
						break;
					case "\n":
					case ",":
						break;
					}
				}
				if (!((Operators.CompareString(text4, "\n", false) == 0) | (Operators.CompareString(text4, "\r", false) == 0)) && ((num <= m_Grid_X) & (num2 <= m_Grid_Y)) && Operators.CompareString(text3, "", false) != 0)
				{
					PasteF(F, (float)Conversion.Val(text3), num, num2);
				}
			}
		}
		if (m_Grid_TransposeCopyPaste == 1)
		{
			Clipboard.Clear();
			Clipboard.SetText(text2);
		}
		Draw_Grid();
		((Control)DataMenuStrip).Hide();
		((Control)this).Focus();
	}

	private void PasteF(int F, float TempF, int XL, int YL)
	{
		if (((SData[checked(XL + YL * (m_Grid_X + 1))] & 1) | (0 - ((MultiSelect < 1) ? 1 : 0))) == 0)
		{
			return;
		}
		checked
		{
			SData[XL + YL * (m_Grid_X + 1)] = (byte)(SData[XL + YL * (m_Grid_X + 1)] | 8);
			if (m_Grid_DataSCopyPaste == 1)
			{
				if (F == 0)
				{
					GData[XL + YL * (m_Grid_X + 1)] = (TempF - m_Grid_DataOffset) / m_Grid_DataScalar;
				}
				if (GData[XL + YL * (m_Grid_X + 1)] < 100000000f)
				{
					if (F == 3)
					{
						GData[XL + YL * (m_Grid_X + 1)] = (GData[XL + YL * (m_Grid_X + 1)] * m_Grid_DataScalar + m_Grid_DataOffset + TempF - m_Grid_DataOffset) / m_Grid_DataScalar;
					}
					if (F == 4)
					{
						GData[XL + YL * (m_Grid_X + 1)] = (GData[XL + YL * (m_Grid_X + 1)] * m_Grid_DataScalar + m_Grid_DataOffset - TempF - m_Grid_DataOffset) / m_Grid_DataScalar;
					}
					if (F == 5)
					{
						GData[XL + YL * (m_Grid_X + 1)] = ((GData[XL + YL * (m_Grid_X + 1)] * m_Grid_DataScalar + m_Grid_DataOffset) * TempF - m_Grid_DataOffset) / m_Grid_DataScalar;
					}
					if (F == 6)
					{
						GData[XL + YL * (m_Grid_X + 1)] = ((GData[XL + YL * (m_Grid_X + 1)] * m_Grid_DataScalar + m_Grid_DataOffset) * (1f + TempF / 100f) - m_Grid_DataOffset) / m_Grid_DataScalar;
					}
					if (F == 7)
					{
						GData[XL + YL * (m_Grid_X + 1)] = (float)(((double)(GData[XL + YL * (m_Grid_X + 1)] * m_Grid_DataScalar + m_Grid_DataOffset) * (1.0 + (double)TempF * 0.5 / 100.0) - (double)m_Grid_DataOffset) / (double)m_Grid_DataScalar);
					}
					if (unchecked(F == 8 && TempF != 0f))
					{
						GData[XL + YL * (m_Grid_X + 1)] = ((GData[XL + YL * (m_Grid_X + 1)] * m_Grid_DataScalar + m_Grid_DataOffset) / TempF - m_Grid_DataOffset) / m_Grid_DataScalar;
					}
					if (F == 9)
					{
						GData[XL + YL * (m_Grid_X + 1)] = ((GData[XL + YL * (m_Grid_X + 1)] * m_Grid_DataScalar + m_Grid_DataOffset + TempF) / 2f - m_Grid_DataOffset) / m_Grid_DataScalar;
					}
				}
				return;
			}
			if (F == 0)
			{
				GData[XL + YL * (m_Grid_X + 1)] = TempF;
			}
			if (GData[XL + YL * (m_Grid_X + 1)] < 100000000f)
			{
				if (F == 3)
				{
					GData[XL + YL * (m_Grid_X + 1)] = GData[XL + YL * (m_Grid_X + 1)] + TempF;
				}
				if (F == 4)
				{
					GData[XL + YL * (m_Grid_X + 1)] = GData[XL + YL * (m_Grid_X + 1)] - TempF;
				}
				if (F == 5)
				{
					GData[XL + YL * (m_Grid_X + 1)] = GData[XL + YL * (m_Grid_X + 1)] * TempF;
				}
				if (F == 6)
				{
					GData[XL + YL * (m_Grid_X + 1)] = GData[XL + YL * (m_Grid_X + 1)] * (1f + TempF / 100f);
				}
				if (F == 7)
				{
					GData[XL + YL * (m_Grid_X + 1)] = (float)((double)GData[XL + YL * (m_Grid_X + 1)] * (1.0 + (double)TempF * 0.5 / 100.0));
				}
				if (unchecked(F == 8 && TempF != 0f))
				{
					GData[XL + YL * (m_Grid_X + 1)] = GData[XL + YL * (m_Grid_X + 1)] / TempF;
				}
				if (F == 9)
				{
					GData[XL + YL * (m_Grid_X + 1)] = (GData[XL + YL * (m_Grid_X + 1)] + TempF) / 2f;
				}
			}
		}
	}

	private void PastewLabels(int F)
	{
		if (m_Grid_ShowLabels == 0)
		{
			return;
		}
		string text = "";
		string text2 = "";
		string text3 = "";
		int num = 1;
		int num2 = 1;
		int num3 = 1;
		int num4 = 1;
		long num5 = 1L;
		int num6 = 1;
		int num7 = 1;
		float num8 = 0f;
		float num9 = 0f;
		float num10 = 0f;
		float num11 = 0f;
		float num12 = 0f;
		float num13 = 0f;
		float num14 = 0f;
		byte b = 0;
		checked
		{
			float[,] array = new float[MAX_X + 1, MAX_Y + 1];
			text = Clipboard.GetText();
			text2 = "";
			long num15 = 1L;
			long num16 = Strings.Len(text);
			for (num5 = num15; num5 <= num16; num5++)
			{
				text3 = Strings.Mid(text, (int)num5, 1);
				switch (text3)
				{
				case "\t":
					if (unchecked(num == 1 && num2 == 1) & (Operators.CompareString(text2, "Labels", false) != 0))
					{
						return;
					}
					if (Operators.CompareString(text2, "", false) == 0)
					{
						array[num, num2] = 100000000f;
					}
					else
					{
						array[num, num2] = (float)Conversion.Val(text2);
					}
					text2 = "";
					num++;
					if (num > num3)
					{
						num3 = num;
					}
					break;
				case "\r":
					if (Operators.CompareString(text2, "", false) == 0)
					{
						array[num, num2] = 100000000f;
					}
					else
					{
						array[num, num2] = (float)Conversion.Val(text2);
					}
					text2 = "";
					num = 1;
					num2++;
					if (num2 > num4)
					{
						num4 = num2;
					}
					break;
				default:
					text2 += text3;
					break;
				case "\n":
				case ",":
					break;
				}
			}
			if (!((Operators.CompareString(text3, "\n", false) == 0) | (Operators.CompareString(text3, "\r", false) == 0)))
			{
				if (Operators.CompareString(text2, "", false) == 0)
				{
					array[num, num2] = 100000000f;
				}
				else
				{
					array[num, num2] = (float)Conversion.Val(text2);
				}
			}
			switch (F)
			{
			case 1:
			{
				int grid_X3 = m_Grid_X;
				for (num6 = 1; num6 <= grid_X3; num6++)
				{
					int grid_Y3 = m_Grid_Y;
					for (num7 = 1; num7 <= grid_Y3; num7++)
					{
						int num21 = num3;
						for (num = 2; num <= num21; num++)
						{
							int num22 = num4;
							for (num2 = 2; num2 <= num22; num2++)
							{
								if (((array[num, 1] == GData[num6 + 0 * (m_Grid_X + 1)]) & (array[1, num2] == GData[0 + num7 * (m_Grid_X + 1)])) && array[num, num2] < 100000000f && ((SData[num6 + num7 * (m_Grid_X + 1)] & 1) | unchecked(0 - ((MultiSelect < 1) ? 1 : 0))) != 0)
								{
									SData[num6 + num7 * (m_Grid_X + 1)] = (byte)(SData[num6 + num7 * (m_Grid_X + 1)] | 8);
									if (m_Grid_DataSCopyPaste == 1)
									{
										GData[num6 + num7 * (m_Grid_X + 1)] = (array[num, num2] - m_Grid_DataOffset) / m_Grid_DataScalar;
									}
									else
									{
										GData[num6 + num7 * (m_Grid_X + 1)] = array[num, num2];
									}
								}
							}
						}
					}
				}
				break;
			}
			case 2:
			{
				if (unchecked(num3 > 2 && num4 > 2))
				{
					int grid_X = m_Grid_X;
					for (num6 = 1; num6 <= grid_X; num6++)
					{
						int grid_Y = m_Grid_Y;
						for (num7 = 1; num7 <= grid_Y; num7++)
						{
							num8 = GData[num6 + 0 * (m_Grid_X + 1)];
							num9 = GData[0 + num7 * (m_Grid_X + 1)];
							int num17 = num3 - 1;
							for (num = 2; num <= num17; num++)
							{
								int num18 = num4 - 1;
								for (num2 = 2; num2 <= num18; num2++)
								{
									if (!((num8 >= array[num, 1]) & (num8 <= array[num + 1, 1]) & (num9 >= array[1, num2]) & (num9 <= array[1, num2 + 1])) || !((array[num, num2] < 100000000f) & (array[num + 1, num2] < 100000000f) & (array[num, num2 + 1] < 100000000f) & (array[num + 1, num2 + 1] < 100000000f)))
									{
										continue;
									}
									b = 0;
									if (array[num + 1, 1] - array[num, 1] == 0f)
									{
										b = 1;
									}
									if (array[1, num2 + 1] - array[1, num2] == 0f)
									{
										b = 1;
									}
									if (b != 0)
									{
										continue;
									}
									num13 = (num8 - array[num, 1]) / (array[num + 1, 1] - array[num, 1]);
									num14 = (num9 - array[1, num2]) / (array[1, num2 + 1] - array[1, num2]);
									num11 = array[num, num2] + (array[num, num2 + 1] - array[num, num2]) * num14;
									num12 = array[num + 1, num2] + (array[num + 1, num2 + 1] - array[num + 1, num2]) * num14;
									num10 = num11 + (num12 - num11) * num13;
									if (((SData[num6 + num7 * (m_Grid_X + 1)] & 1) | unchecked(0 - ((MultiSelect < 1) ? 1 : 0))) != 0)
									{
										SData[num6 + num7 * (m_Grid_X + 1)] = (byte)(SData[num6 + num7 * (m_Grid_X + 1)] | 8);
										if (m_Grid_DataSCopyPaste == 1)
										{
											GData[num6 + num7 * (m_Grid_X + 1)] = (num10 - m_Grid_DataOffset) / m_Grid_DataScalar;
										}
										else
										{
											GData[num6 + num7 * (m_Grid_X + 1)] = num10;
										}
									}
								}
							}
						}
					}
				}
				if (num4 == 2)
				{
					num2 = 2;
					int grid_X2 = m_Grid_X;
					for (num6 = 1; num6 <= grid_X2; num6++)
					{
						num7 = LY;
						if (num7 < 1)
						{
							num7 = 1;
						}
						num8 = GData[num6 + 0 * (m_Grid_X + 1)];
						int num19 = num3 - 1;
						for (num = 2; num <= num19; num++)
						{
							if (!((num8 >= array[num, 1]) & (num8 <= array[num + 1, 1])) || !((array[num, num2] < 100000000f) & (array[num + 1, num2] < 100000000f)))
							{
								continue;
							}
							b = 0;
							if (array[num + 1, 1] - array[num, 1] == 0f)
							{
								b = 1;
							}
							if (b != 0)
							{
								continue;
							}
							num13 = (num8 - array[num, 1]) / (array[num + 1, 1] - array[num, 1]);
							num11 = array[num, num2];
							num12 = array[num + 1, num2];
							num10 = num11 + (num12 - num11) * num13;
							if (((SData[num6 + num7 * (m_Grid_X + 1)] & 1) | unchecked(0 - ((MultiSelect < 1) ? 1 : 0))) != 0)
							{
								SData[num6 + num7 * (m_Grid_X + 1)] = (byte)(SData[num6 + num7 * (m_Grid_X + 1)] | 8);
								if (m_Grid_DataSCopyPaste == 1)
								{
									GData[num6 + num7 * (m_Grid_X + 1)] = (num10 - m_Grid_DataOffset) / m_Grid_DataScalar;
								}
								else
								{
									GData[num6 + num7 * (m_Grid_X + 1)] = num10;
								}
							}
						}
					}
				}
				if (num3 != 2)
				{
					break;
				}
				num = 2;
				num6 = LX;
				if (num6 < 1)
				{
					num6 = 1;
				}
				int grid_Y2 = m_Grid_Y;
				for (num7 = 1; num7 <= grid_Y2; num7++)
				{
					num9 = GData[0 + num7 * (m_Grid_X + 1)];
					int num20 = num4 - 1;
					for (num2 = 2; num2 <= num20; num2++)
					{
						if (!((num9 >= array[1, num2]) & (num9 <= array[1, num2 + 1])) || !((array[num, num2 + 1] < 100000000f) & (array[num + 1, num2 + 1] < 100000000f)))
						{
							continue;
						}
						b = 0;
						if (array[num + 1, 1] - array[num, 1] == 0f)
						{
							b = 1;
						}
						if (array[1, num2 + 1] - array[1, num2] == 0f)
						{
							b = 1;
						}
						if (b != 0)
						{
							continue;
						}
						num14 = (num9 - array[1, num2]) / (array[1, num2 + 1] - array[1, num2]);
						num10 = array[num, num2] + (array[num, num2 + 1] - array[num, num2]) * num14;
						if (((SData[num6 + num7 * (m_Grid_X + 1)] & 1) | unchecked(0 - ((MultiSelect < 1) ? 1 : 0))) != 0)
						{
							SData[num6 + num7 * (m_Grid_X + 1)] = (byte)(SData[num6 + num7 * (m_Grid_X + 1)] | 8);
							if (m_Grid_DataSCopyPaste == 1)
							{
								GData[num6 + num7 * (m_Grid_X + 1)] = (num10 - m_Grid_DataOffset) / m_Grid_DataScalar;
							}
							else
							{
								GData[num6 + num7 * (m_Grid_X + 1)] = num10;
							}
						}
					}
				}
				break;
			}
			}
		}
	}

	public void TransposeClipboard()
	{
		string text = "";
		string text2 = "";
		string text3 = "";
		int num = 1;
		int num2 = 1;
		int num3 = 1;
		int num4 = 1;
		long num5 = 1L;
		byte b = 0;
		int mAX_X = MAX_X;
		int num6 = 0;
		int mAX_Y = MAX_Y;
		int num7 = 0;
		checked
		{
			float[,] array = new float[MAX_X + 1, MAX_Y + 1];
			text = Clipboard.GetText();
			text2 = "";
			long num8 = 1L;
			long num9 = Strings.Len(text);
			for (num5 = num8; num5 <= num9; num5++)
			{
				text3 = Strings.Mid(text, (int)num5, 1);
				switch (text3)
				{
				case "\t":
					if (unchecked(num == 1 && num2 == 1) & (Operators.CompareString(text2, "Labels", false) == 0))
					{
						b = 1;
					}
					if (Operators.CompareString(text2, "", false) == 0)
					{
						array[num, num2] = 100000000f;
					}
					else
					{
						array[num, num2] = (float)Conversion.Val(text2);
					}
					text2 = "";
					num++;
					if (num > num3)
					{
						num3 = num;
					}
					break;
				case "\r":
					if (Operators.CompareString(text2, "", false) == 0)
					{
						array[num, num2] = 100000000f;
					}
					else
					{
						array[num, num2] = (float)Conversion.Val(text2);
					}
					text2 = "";
					num = 1;
					num2++;
					if (num2 > num4)
					{
						num4 = num2;
					}
					break;
				default:
					text2 += text3;
					break;
				case "\n":
				case ",":
					break;
				}
			}
			if (!((Operators.CompareString(text3, "\n", false) == 0) | (Operators.CompareString(text3, "\r", false) == 0)))
			{
				if (Operators.CompareString(text2, "", false) == 0)
				{
					array[num, num2] = 100000000f;
				}
				else
				{
					array[num, num2] = (float)Conversion.Val(text2);
				}
			}
			mAX_X = 1;
			num6 = num3;
			mAX_Y = 1;
			num7 = num4;
			text = "";
			int num10 = mAX_X;
			int num11 = num6;
			for (int i = num10; i <= num11; i++)
			{
				int num12 = mAX_Y;
				int num13 = num7;
				for (int j = num12; j <= num13; j++)
				{
					unchecked
					{
						if (!(array[i, j] >= 100000000f))
						{
							text = ((!(b == 1 && i == 1 && j == 1)) ? (text + Strings.Format((object)array[i, j], "")) : (text + "Labels"));
						}
						if (!(j == num7 && i == num6))
						{
							text = ((j != num7) ? (text + "\t") : (text + "\r\n"));
						}
					}
				}
			}
			Clipboard.Clear();
			if (Operators.CompareString(text, "", false) != 0)
			{
				Clipboard.SetText(text);
			}
		}
	}

	public void X_Scale_Clipboard(float SF)
	{
		string text = "";
		string text2 = "";
		string text3 = "";
		int num = 1;
		int num2 = 1;
		int num3 = 1;
		int num4 = 1;
		long num5 = 1L;
		byte b = 0;
		int mAX_X = MAX_X;
		int num6 = 0;
		int mAX_Y = MAX_Y;
		int num7 = 0;
		checked
		{
			float[,] array = new float[MAX_X + 1, MAX_Y + 1];
			text = Clipboard.GetText();
			text2 = "";
			long num8 = 1L;
			long num9 = Strings.Len(text);
			for (num5 = num8; num5 <= num9; num5++)
			{
				text3 = Strings.Mid(text, (int)num5, 1);
				switch (text3)
				{
				case "\t":
					unchecked
					{
						if ((num == 1 && num2 == 1) & (Operators.CompareString(text2, "Labels", false) != 0))
						{
							return;
						}
						if ((num == 1 && num2 == 1) & (Operators.CompareString(text2, "Labels", false) == 0))
						{
							b = 1;
						}
						if (Operators.CompareString(text2, "", false) == 0)
						{
							array[num, num2] = 100000000f;
						}
						else
						{
							array[num, num2] = (float)Conversion.Val(text2);
						}
						text2 = "";
					}
					num++;
					if (num > num3)
					{
						num3 = num;
					}
					break;
				case "\r":
					if (Operators.CompareString(text2, "", false) == 0)
					{
						array[num, num2] = 100000000f;
					}
					else
					{
						array[num, num2] = (float)Conversion.Val(text2);
					}
					text2 = "";
					num = 1;
					num2++;
					if (num2 > num4)
					{
						num4 = num2;
					}
					break;
				default:
					text2 += text3;
					break;
				case "\n":
				case ",":
					break;
				}
			}
			if (!((Operators.CompareString(text3, "\n", false) == 0) | (Operators.CompareString(text3, "\r", false) == 0)))
			{
				if (Operators.CompareString(text2, "", false) == 0)
				{
					array[num, num2] = 100000000f;
				}
				else
				{
					array[num, num2] = (float)Conversion.Val(text2);
				}
			}
			mAX_X = 1;
			num6 = num3;
			mAX_Y = 1;
			num7 = num4;
			text = "";
			int num10 = mAX_Y;
			int num11 = num7;
			for (int i = num10; i <= num11; i++)
			{
				int num12 = mAX_X;
				int num13 = num6;
				for (int j = num12; j <= num13; j++)
				{
					unchecked
					{
						if (!(array[j, i] >= 100000000f))
						{
							text = ((b == 1 && j == 1 && i == 1) ? (text + "Labels") : ((!(b == 1 && i == 1)) ? (text + Strings.Format((object)array[j, i], "")) : (text + Strings.Format((object)(array[j, i] * SF), ""))));
						}
						if (!(i == num7 && j == num6))
						{
							text = ((j != num6) ? (text + "\t") : (text + "\r\n"));
						}
					}
				}
			}
			Clipboard.Clear();
			if (Operators.CompareString(text, "", false) != 0)
			{
				Clipboard.SetText(text);
			}
		}
	}

	public void Y_Scale_Clipboard(float SF)
	{
		string text = "";
		string text2 = "";
		string text3 = "";
		int num = 1;
		int num2 = 1;
		int num3 = 1;
		int num4 = 1;
		long num5 = 1L;
		byte b = 0;
		int mAX_X = MAX_X;
		int num6 = 0;
		int mAX_Y = MAX_Y;
		int num7 = 0;
		checked
		{
			float[,] array = new float[MAX_X + 1, MAX_Y + 1];
			text = Clipboard.GetText();
			text2 = "";
			long num8 = 1L;
			long num9 = Strings.Len(text);
			for (num5 = num8; num5 <= num9; num5++)
			{
				text3 = Strings.Mid(text, (int)num5, 1);
				switch (text3)
				{
				case "\t":
					unchecked
					{
						if ((num == 1 && num2 == 1) & (Operators.CompareString(text2, "Labels", false) != 0))
						{
							return;
						}
						if ((num == 1 && num2 == 1) & (Operators.CompareString(text2, "Labels", false) == 0))
						{
							b = 1;
						}
						if (Operators.CompareString(text2, "", false) == 0)
						{
							array[num, num2] = 100000000f;
						}
						else
						{
							array[num, num2] = (float)Conversion.Val(text2);
						}
						text2 = "";
					}
					num++;
					if (num > num3)
					{
						num3 = num;
					}
					break;
				case "\r":
					if (Operators.CompareString(text2, "", false) == 0)
					{
						array[num, num2] = 100000000f;
					}
					else
					{
						array[num, num2] = (float)Conversion.Val(text2);
					}
					text2 = "";
					num = 1;
					num2++;
					if (num2 > num4)
					{
						num4 = num2;
					}
					break;
				default:
					text2 += text3;
					break;
				case "\n":
				case ",":
					break;
				}
			}
			if (!((Operators.CompareString(text3, "\n", false) == 0) | (Operators.CompareString(text3, "\r", false) == 0)))
			{
				if (Operators.CompareString(text2, "", false) == 0)
				{
					array[num, num2] = 100000000f;
				}
				else
				{
					array[num, num2] = (float)Conversion.Val(text2);
				}
			}
			mAX_X = 1;
			num6 = num3;
			mAX_Y = 1;
			num7 = num4;
			text = "";
			int num10 = mAX_Y;
			int num11 = num7;
			for (int i = num10; i <= num11; i++)
			{
				int num12 = mAX_X;
				int num13 = num6;
				for (int j = num12; j <= num13; j++)
				{
					unchecked
					{
						if (!(array[j, i] >= 100000000f))
						{
							text = ((b == 1 && j == 1 && i == 1) ? (text + "Labels") : ((!(b == 1 && j == 1)) ? (text + Strings.Format((object)array[j, i], "")) : (text + Strings.Format((object)(array[j, i] * SF), ""))));
						}
						if (!(i == num7 && j == num6))
						{
							text = ((j != num6) ? (text + "\t") : (text + "\r\n"));
						}
					}
				}
			}
			Clipboard.Clear();
			if (Operators.CompareString(text, "", false) != 0)
			{
				Clipboard.SetText(text);
			}
		}
	}

	public void Import_Axes_Clipboard()
	{
		if (m_Grid_AxisStatus == -1)
		{
			return;
		}
		string text = "";
		string text2 = "";
		string text3 = "";
		int num = 1;
		int num2 = 1;
		int num3 = 1;
		int num4 = 1;
		long num5 = 1L;
		byte b = 0;
		int mAX_X = MAX_X;
		int num6 = 0;
		int mAX_Y = MAX_Y;
		int num7 = 0;
		checked
		{
			float[,] array = new float[MAX_X + 1, MAX_Y + 1];
			text = Clipboard.GetText();
			text2 = "";
			long num8 = 1L;
			long num9 = Strings.Len(text);
			for (num5 = num8; num5 <= num9; num5++)
			{
				text3 = Strings.Mid(text, (int)num5, 1);
				switch (text3)
				{
				case "\t":
					unchecked
					{
						if ((num == 1 && num2 == 1) & (Operators.CompareString(text2, "Labels", false) != 0))
						{
							return;
						}
						if ((num == 1 && num2 == 1) & (Operators.CompareString(text2, "Labels", false) == 0))
						{
							b = 1;
						}
						if (Operators.CompareString(text2, "", false) == 0)
						{
							array[num, num2] = 100000000f;
						}
						else
						{
							array[num, num2] = (float)Conversion.Val(text2);
						}
						text2 = "";
					}
					num++;
					if (num > num3)
					{
						num3 = num;
					}
					break;
				case "\r":
					if (Operators.CompareString(text2, "", false) == 0)
					{
						array[num, num2] = 100000000f;
					}
					else
					{
						array[num, num2] = (float)Conversion.Val(text2);
					}
					text2 = "";
					num = 1;
					num2++;
					if (num2 > num4)
					{
						num4 = num2;
					}
					break;
				default:
					text2 += text3;
					break;
				case "\n":
				case ",":
					break;
				}
			}
			if (!((Operators.CompareString(text3, "\n", false) == 0) | (Operators.CompareString(text3, "\r", false) == 0)))
			{
				if (Operators.CompareString(text2, "", false) == 0)
				{
					array[num, num2] = 100000000f;
				}
				else
				{
					array[num, num2] = (float)Conversion.Val(text2);
				}
			}
			mAX_X = 1;
			num6 = num3;
			mAX_Y = 1;
			num7 = num4;
			text = "";
			Grid_X = num3 - 1;
			int grid_X = m_Grid_X;
			for (int i = 1; i <= grid_X; i++)
			{
				GData[i + 0 * (m_Grid_X + 1)] = array[i + 1, 1];
			}
			Grid_Y = num4 - 1;
			int grid_Y = m_Grid_Y;
			for (int i = 1; i <= grid_Y; i++)
			{
				GData[0 + i * (m_Grid_X + 1)] = array[1, i + 1];
			}
			m_Grid_AxisStatus++;
			if (m_Grid_AxisStatus > 30000)
			{
				m_Grid_AxisStatus = 0;
			}
			Draw_Grid();
		}
	}

	public void Interpolate(int F)
	{
		if (F == 3)
		{
			F = 0;
		}
		else
		{
			SaveUndo();
		}
		checked
		{
			byte b;
			do
			{
				b = 0;
				int grid_X = m_Grid_X;
				for (int i = 1; i <= grid_X; i++)
				{
					int grid_Y = m_Grid_Y;
					for (int j = 1; j <= grid_Y; j++)
					{
						if ((SData[i + j * (m_Grid_X + 1)] & 1) == 0)
						{
							continue;
						}
						int num = i;
						while (true)
						{
							num--;
							if (num < 1)
							{
								num = -1;
								break;
							}
							if ((unchecked((byte)(~SData[checked(num + j * (m_Grid_X + 1))])) & 1) != 0)
							{
								if (GData[num + j * (m_Grid_X + 1)] > 100000000f)
								{
									num = -1;
								}
								break;
							}
						}
						int num2 = i;
						while (true)
						{
							num2++;
							if (num2 > m_Grid_X)
							{
								num2 = -1;
								break;
							}
							if ((unchecked((byte)(~SData[checked(num2 + j * (m_Grid_X + 1))])) & 1) != 0)
							{
								if (GData[num2 + j * (m_Grid_X + 1)] > 100000000f)
								{
									num2 = -1;
								}
								break;
							}
						}
						int num3 = j;
						while (true)
						{
							num3--;
							if (num3 < 1)
							{
								num3 = -1;
								break;
							}
							if ((unchecked((byte)(~SData[checked(i + num3 * (m_Grid_X + 1))])) & 1) != 0)
							{
								if (GData[i + num3 * (m_Grid_X + 1)] > 100000000f)
								{
									num3 = -1;
								}
								break;
							}
						}
						int num4 = j;
						while (true)
						{
							num4++;
							if (num4 > m_Grid_Y)
							{
								num4 = -1;
								break;
							}
							if ((unchecked((byte)(~SData[checked(i + num4 * (m_Grid_X + 1))])) & 1) != 0)
							{
								if (GData[i + num4 * (m_Grid_X + 1)] > 100000000f)
								{
									num4 = -1;
								}
								break;
							}
						}
						double num5 = 0.0;
						float num6 = 0f;
						if (unchecked(F == 1 || F == 0))
						{
							if (unchecked(num != -1 && num2 != -1))
							{
								if ((GData[num + j * (m_Grid_X + 1)] < 100000000f) & (GData[num2 + j * (m_Grid_X + 1)] < 100000000f))
								{
									double num7 = (double)(i - num) / (double)(num2 - num);
									num7 = (double)GData[num + j * (m_Grid_X + 1)] + (double)(GData[num2 + j * (m_Grid_X + 1)] - GData[num + j * (m_Grid_X + 1)]) * num7;
									num5 += num7;
									num6 += 1f;
								}
							}
							else if (unchecked(num2 == -1 && num > 1))
							{
								if ((GData[num + j * (m_Grid_X + 1)] < 100000000f) & (GData[num - 1 + j * (m_Grid_X + 1)] < 100000000f))
								{
									double num7 = GData[num + j * (m_Grid_X + 1)] - GData[num - 1 + j * (m_Grid_X + 1)];
									num7 = (double)GData[num + j * (m_Grid_X + 1)] + num7 * (double)(i - num);
									num5 += num7;
									num6 += 1f;
								}
							}
							else if (unchecked(((num == -1) & (num2 < m_Grid_X)) && num2 != -1) && ((GData[num2 + j * (m_Grid_X + 1)] < 100000000f) & (GData[num2 + 1 + j * (m_Grid_X + 1)] < 100000000f)))
							{
								double num7 = GData[num2 + j * (m_Grid_X + 1)] - GData[num2 + 1 + j * (m_Grid_X + 1)];
								num7 = (double)GData[num2 + j * (m_Grid_X + 1)] + num7 * (double)(num2 - i);
								num5 += num7;
								num6 += 1f;
							}
						}
						if (unchecked(F == 2 || F == 0))
						{
							if (unchecked(num3 != -1 && num4 != -1))
							{
								if ((GData[i + num3 * (m_Grid_X + 1)] < 100000000f) & (GData[i + num4 * (m_Grid_X + 1)] < 100000000f))
								{
									double num7 = (double)(j - num3) / (double)(num4 - num3);
									num7 = (double)GData[i + num3 * (m_Grid_X + 1)] + (double)(GData[i + num4 * (m_Grid_X + 1)] - GData[i + num3 * (m_Grid_X + 1)]) * num7;
									num5 += num7;
									num6 += 1f;
								}
							}
							else if (unchecked(num4 == -1 && num3 > 1))
							{
								if ((GData[i + num3 * (m_Grid_X + 1)] < 100000000f) & (GData[i + (num3 - 1) * (m_Grid_X + 1)] < 100000000f))
								{
									double num7 = GData[i + num3 * (m_Grid_X + 1)] - GData[i + (num3 - 1) * (m_Grid_X + 1)];
									num7 = (double)GData[i + num3 * (m_Grid_X + 1)] + num7 * (double)(j - num3);
									num5 += num7;
									num6 += 1f;
								}
							}
							else if (unchecked(((num3 == -1) & (num4 < m_Grid_Y)) && num4 != -1) && ((GData[i + num4 * (m_Grid_X + 1)] < 100000000f) & (GData[i + (num4 + 1) * (m_Grid_X + 1)] < 100000000f)))
							{
								double num7 = GData[i + num4 * (m_Grid_X + 1)] - GData[i + (num4 + 1) * (m_Grid_X + 1)];
								num7 = (double)GData[i + num4 * (m_Grid_X + 1)] + num7 * (double)(num4 - j);
								num5 += num7;
								num6 += 1f;
							}
						}
						if (num6 != 0f)
						{
							SData[i + j * (m_Grid_X + 1)] = (byte)(SData[i + j * (m_Grid_X + 1)] | 8);
							GData[i + j * (m_Grid_X + 1)] = (float)(num5 / (double)num6);
							SData[i + j * (m_Grid_X + 1)] = (byte)(SData[i + j * (m_Grid_X + 1)] | 4);
							b = 1;
						}
					}
				}
				int grid_X2 = m_Grid_X;
				for (int i = 1; i <= grid_X2; i++)
				{
					int grid_Y2 = m_Grid_Y;
					for (int j = 1; j <= grid_Y2; j++)
					{
						if ((SData[i + j * (m_Grid_X + 1)] & 4) != 0)
						{
							SData[i + j * (m_Grid_X + 1)] = (byte)(SData[i + j * (m_Grid_X + 1)] & -2);
						}
					}
				}
			}
			while (b == 1);
			int grid_X3 = m_Grid_X;
			for (int i = 1; i <= grid_X3; i++)
			{
				int grid_Y3 = m_Grid_Y;
				for (int j = 1; j <= grid_Y3; j++)
				{
					if ((SData[i + j * (m_Grid_X + 1)] & 4) != 0)
					{
						SData[i + j * (m_Grid_X + 1)] = (byte)(SData[i + j * (m_Grid_X + 1)] & -5);
						SData[i + j * (m_Grid_X + 1)] = (byte)(SData[i + j * (m_Grid_X + 1)] | 1);
					}
				}
			}
		}
	}

	public void Extrapolate()
	{
		SaveUndo();
		checked
		{
			byte b;
			do
			{
				b = 0;
				int grid_X = m_Grid_X;
				for (int i = 1; i <= grid_X; i++)
				{
					int grid_Y = m_Grid_Y;
					for (int j = 1; j <= grid_Y; j++)
					{
						if ((SData[i + j * (m_Grid_X + 1)] & 1) == 0)
						{
							continue;
						}
						int num = i;
						while (true)
						{
							num--;
							if (num < 1)
							{
								num = -1;
								break;
							}
							if ((unchecked((byte)(~SData[checked(num + j * (m_Grid_X + 1))])) & 1) != 0)
							{
								if (GData[num + j * (m_Grid_X + 1)] > 100000000f)
								{
									num = -1;
								}
								break;
							}
						}
						int num2 = i;
						while (true)
						{
							num2++;
							if (num2 > m_Grid_X)
							{
								num2 = -1;
								break;
							}
							if ((unchecked((byte)(~SData[checked(num2 + j * (m_Grid_X + 1))])) & 1) != 0)
							{
								if (GData[num2 + j * (m_Grid_X + 1)] > 100000000f)
								{
									num2 = -1;
								}
								break;
							}
						}
						int num3 = j;
						while (true)
						{
							num3--;
							if (num3 < 1)
							{
								num3 = -1;
								break;
							}
							if ((unchecked((byte)(~SData[checked(i + num3 * (m_Grid_X + 1))])) & 1) != 0)
							{
								if (GData[i + num3 * (m_Grid_X + 1)] > 100000000f)
								{
									num3 = -1;
								}
								break;
							}
						}
						int num4 = j;
						while (true)
						{
							num4++;
							if (num4 > m_Grid_Y)
							{
								num4 = -1;
								break;
							}
							if ((unchecked((byte)(~SData[checked(i + num4 * (m_Grid_X + 1))])) & 1) != 0)
							{
								if (GData[i + num4 * (m_Grid_X + 1)] > 100000000f)
								{
									num4 = -1;
								}
								break;
							}
						}
						double num5 = 0.0;
						float num6 = 0f;
						if (unchecked(num4 != -1 && num != -1) && ((GData[num + num4 * (m_Grid_X + 1)] != 0f) & (GData[num + num4 * (m_Grid_X + 1)] < 100000000f) & (GData[i + num4 * (m_Grid_X + 1)] < 100000000f) & (GData[num + j * (m_Grid_X + 1)] < 100000000f)))
						{
							if ((SData[num + num4 * (m_Grid_X + 1)] & 1) != 0)
							{
								continue;
							}
							double num7 = GData[i + num4 * (m_Grid_X + 1)] * GData[num + j * (m_Grid_X + 1)];
							num7 /= (double)GData[num + num4 * (m_Grid_X + 1)];
							float num8 = (float)(1.0 / (double)(i - num));
							num8 = (float)((double)num8 + 1.0 / (double)(num4 - j));
							num5 += num7 * (double)num8;
							num6 += num8;
						}
						if (unchecked(num3 != -1 && num != -1) && ((GData[num + num3 * (m_Grid_X + 1)] != 0f) & (GData[num + num3 * (m_Grid_X + 1)] < 100000000f) & (GData[i + num3 * (m_Grid_X + 1)] < 100000000f) & (GData[num + j * (m_Grid_X + 1)] < 100000000f)))
						{
							if ((SData[num + num3 * (m_Grid_X + 1)] & 1) != 0)
							{
								continue;
							}
							double num7 = GData[i + num3 * (m_Grid_X + 1)] * GData[num + j * (m_Grid_X + 1)];
							num7 /= (double)GData[num + num3 * (m_Grid_X + 1)];
							float num8 = (float)(1.0 / (double)(i - num));
							num8 = (float)((double)num8 + 1.0 / (double)(j - num3));
							num5 += num7 * (double)num8;
							num6 += num8;
						}
						if (unchecked(num3 != -1 && num2 != -1) && ((GData[num2 + num3 * (m_Grid_X + 1)] != 0f) & (GData[num2 + num3 * (m_Grid_X + 1)] < 100000000f) & (GData[i + num3 * (m_Grid_X + 1)] < 100000000f) & (GData[num2 + j * (m_Grid_X + 1)] < 100000000f)))
						{
							if ((SData[num2 + num3 * (m_Grid_X + 1)] & 1) != 0)
							{
								continue;
							}
							double num7 = GData[i + num3 * (m_Grid_X + 1)] * GData[num2 + j * (m_Grid_X + 1)];
							num7 /= (double)GData[num2 + num3 * (m_Grid_X + 1)];
							float num8 = (float)(1.0 / (double)(num2 - i));
							num8 = (float)((double)num8 + 1.0 / (double)(j - num3));
							num5 += num7 * (double)num8;
							num6 += num8;
						}
						if (unchecked(num4 != -1 && num2 != -1) && ((GData[num2 + num4 * (m_Grid_X + 1)] != 0f) & (GData[num2 + num4 * (m_Grid_X + 1)] < 100000000f) & (GData[i + num4 * (m_Grid_X + 1)] < 100000000f) & (GData[num2 + j * (m_Grid_X + 1)] < 100000000f)))
						{
							if ((SData[num2 + num4 * (m_Grid_X + 1)] & 1) != 0)
							{
								continue;
							}
							double num7 = GData[i + num4 * (m_Grid_X + 1)] * GData[num2 + j * (m_Grid_X + 1)];
							num7 /= (double)GData[num2 + num4 * (m_Grid_X + 1)];
							float num8 = (float)(1.0 / (double)(num2 - i));
							num8 = (float)((double)num8 + 1.0 / (double)(num4 - j));
							num5 += num7 * (double)num8;
							num6 += num8;
						}
						if (num6 != 0f)
						{
							SData[i + j * (m_Grid_X + 1)] = (byte)(SData[i + j * (m_Grid_X + 1)] | 8);
							GData[i + j * (m_Grid_X + 1)] = (float)(num5 / (double)num6);
							SData[i + j * (m_Grid_X + 1)] = (byte)(SData[i + j * (m_Grid_X + 1)] | 4);
							b = 1;
						}
					}
				}
				int grid_X2 = m_Grid_X;
				for (int i = 1; i <= grid_X2; i++)
				{
					int grid_Y2 = m_Grid_Y;
					for (int j = 1; j <= grid_Y2; j++)
					{
						if ((SData[i + j * (m_Grid_X + 1)] & 4) != 0)
						{
							SData[i + j * (m_Grid_X + 1)] = (byte)(SData[i + j * (m_Grid_X + 1)] & -2);
						}
					}
				}
			}
			while (b == 1);
			Interpolate(3);
			int grid_X3 = m_Grid_X;
			for (int i = 1; i <= grid_X3; i++)
			{
				int grid_Y3 = m_Grid_Y;
				for (int j = 1; j <= grid_Y3; j++)
				{
					if ((SData[i + j * (m_Grid_X + 1)] & 4) != 0)
					{
						SData[i + j * (m_Grid_X + 1)] = (byte)(SData[i + j * (m_Grid_X + 1)] & -5);
						SData[i + j * (m_Grid_X + 1)] = (byte)(SData[i + j * (m_Grid_X + 1)] | 1);
					}
				}
			}
		}
	}

	public void Smooth(int F)
	{
		SaveUndo();
		checked
		{
			float[,] array = new float[MAX_X + 1, MAX_Y + 1];
			int num = 1;
			int num2 = 1;
			int num3 = 0;
			float num4 = 0f;
			int grid_X = m_Grid_X;
			for (num = 1; num <= grid_X; num++)
			{
				int grid_Y = m_Grid_Y;
				for (num2 = 1; num2 <= grid_Y; num2++)
				{
					array[num, num2] = GData[num + num2 * (m_Grid_X + 1)];
				}
			}
			int grid_X2 = m_Grid_X;
			for (num = 1; num <= grid_X2; num++)
			{
				int grid_Y2 = m_Grid_Y;
				for (num2 = 1; num2 <= grid_Y2; num2++)
				{
					num3 = 0;
					num4 = 0f;
					if (((SData[num + num2 * (m_Grid_X + 1)] & 1) | unchecked(0 - ((MultiSelect == -1) ? 1 : 0))) != 0)
					{
						num4 += array[num, num2];
						num3++;
						num4 += array[num, num2];
						num3++;
						num4 += array[num, num2];
						num3++;
						num4 += array[num, num2];
						num3++;
						num4 += array[num, num2];
						num3++;
						num4 += array[num, num2];
						num3++;
						if (unchecked(F == 1 || F == 0) && ((num - 1 >= 1) & (num + 1 <= m_Grid_X) & (array[num - 1, num2] < 100000000f) & (array[num + 1, num2] < 100000000f)))
						{
							num4 += array[num - 1, num2];
							num3++;
							num4 += array[num, num2];
							num3++;
							num4 += array[num + 1, num2];
							num3++;
							num4 += array[num, num2];
							num3++;
						}
						if (unchecked(F == 2 || F == 0) && ((num2 - 1 >= 1) & (num2 + 1 <= m_Grid_Y) & (array[num, num2 - 1] < 100000000f) & (array[num, num2 + 1] < 100000000f)))
						{
							num4 += array[num, num2 - 1];
							num3++;
							num4 += array[num, num2];
							num3++;
							num4 += array[num, num2 + 1];
							num3++;
							num4 += array[num, num2];
							num3++;
						}
						if (F == 0 && ((num - 1 >= 1) & (num + 1 <= m_Grid_X) & (num2 - 1 >= 1) & (num2 + 1 <= m_Grid_Y) & (array[num - 1, num2 - 1] < 100000000f) & (array[num + 1, num2 - 1] < 100000000f) & (array[num - 1, num2 + 1] < 100000000f) & (array[num + 1, num2 + 1] < 100000000f)))
						{
							num4 += array[num - 1, num2 - 1];
							num3++;
							num4 += array[num + 1, num2 - 1];
							num3++;
							num4 += array[num, num2];
							num3++;
							num4 += array[num - 1, num2 + 1];
							num3++;
							num4 += array[num + 1, num2 + 1];
							num3++;
							num4 += array[num, num2];
							num3++;
						}
						if (num3 > 0)
						{
							SData[num + num2 * (m_Grid_X + 1)] = (byte)(SData[num + num2 * (m_Grid_X + 1)] | 8);
							num4 /= (float)num3;
							GData[num + num2 * (m_Grid_X + 1)] = num4;
						}
					}
				}
			}
		}
	}

	private void Grid_Math(float X, int M)
	{
		SaveUndo();
		int grid_X = m_Grid_X;
		checked
		{
			for (int i = 1; i <= grid_X; i++)
			{
				int grid_Y = m_Grid_Y;
				for (int j = 1; j <= grid_Y; j++)
				{
					if ((SData[i + j * (m_Grid_X + 1)] & 1) == 0)
					{
						continue;
					}
					SData[i + j * (m_Grid_X + 1)] = (byte)(SData[i + j * (m_Grid_X + 1)] | 8);
					if (M == 0)
					{
						GData[i + j * (m_Grid_X + 1)] = (X - m_Grid_DataOffset) / m_Grid_DataScalar;
					}
					if (GData[i + j * (m_Grid_X + 1)] < 100000000f)
					{
						if (M == 1)
						{
							GData[i + j * (m_Grid_X + 1)] = (GData[i + j * (m_Grid_X + 1)] * m_Grid_DataScalar + m_Grid_DataOffset + X - m_Grid_DataOffset) / m_Grid_DataScalar;
						}
						if (M == 2)
						{
							GData[i + j * (m_Grid_X + 1)] = (GData[i + j * (m_Grid_X + 1)] * m_Grid_DataScalar + m_Grid_DataOffset - X - m_Grid_DataOffset) / m_Grid_DataScalar;
						}
						if (M == 3)
						{
							GData[i + j * (m_Grid_X + 1)] = ((GData[i + j * (m_Grid_X + 1)] * m_Grid_DataScalar + m_Grid_DataOffset) * X - m_Grid_DataOffset) / m_Grid_DataScalar;
						}
						if (unchecked(M == 4 && X != 0f))
						{
							GData[i + j * (m_Grid_X + 1)] = ((GData[i + j * (m_Grid_X + 1)] * m_Grid_DataScalar + m_Grid_DataOffset) / X - m_Grid_DataOffset) / m_Grid_DataScalar;
						}
					}
				}
			}
		}
	}

	private void ToolbarToolStripMenuItem_Click(object sender, EventArgs e)
	{
		((Control)Toolbar).Show();
		Toolbar.Location = ((Control)this).PointToScreen(Point.Empty);
		((Control)Toolbar).Top = checked(((Control)Toolbar).Top - ((Control)Toolbar).Height);
		((Control)DataMenuStrip).Hide();
	}

	private void Toolbar_Closing(object sender, CancelEventArgs e)
	{
		e.Cancel = true;
		((Control)Toolbar).Hide();
	}

	private void TB_Text1_KeyPress(object sender, KeyPressEventArgs e)
	{
		if (e.KeyChar == '\r')
		{
			e.Handled = true;
			Grid_Math((float)Conversion.Val(TB_Text1.Text), 0);
			Draw_Grid();
		}
	}

	private void TB_Btn1_Click(object sender, EventArgs e)
	{
		Grid_Math((float)Conversion.Val(TB_Text1.Text), 0);
		Draw_Grid();
	}

	private void TB_Btn2_Click(object sender, EventArgs e)
	{
		Grid_Math((float)Conversion.Val(TB_Text1.Text), 1);
		Draw_Grid();
	}

	private void TB_Btn3_Click(object sender, EventArgs e)
	{
		Grid_Math((float)Conversion.Val(TB_Text1.Text), 2);
		Draw_Grid();
	}

	private void TB_Btn4_Click(object sender, EventArgs e)
	{
		Grid_Math((float)Conversion.Val(TB_Text1.Text), 3);
		Draw_Grid();
	}

	private void TB_Btn5_Click(object sender, EventArgs e)
	{
		Grid_Math((float)Conversion.Val(TB_Text1.Text), 4);
		Draw_Grid();
	}

	private void TB_Btn6_Click(object sender, EventArgs e)
	{
		Smooth(0);
		Draw_Grid();
	}

	private void TB_Btn7_Click(object sender, EventArgs e)
	{
		if (m_Grid_Transpose == 1)
		{
			Smooth(2);
		}
		else
		{
			Smooth(1);
		}
		Draw_Grid();
	}

	private void TB_Btn8_Click(object sender, EventArgs e)
	{
		if (m_Grid_Transpose == 1)
		{
			Smooth(1);
		}
		else
		{
			Smooth(2);
		}
		Draw_Grid();
	}

	private void TB_Btn9_Click(object sender, EventArgs e)
	{
		Interpolate(0);
		Draw_Grid();
	}

	private void TB_Btn10_Click(object sender, EventArgs e)
	{
		if (m_Grid_Transpose == 1)
		{
			Interpolate(2);
		}
		else
		{
			Interpolate(1);
		}
		Draw_Grid();
	}

	private void TB_Btn11_Click(object sender, EventArgs e)
	{
		if (m_Grid_Transpose == 1)
		{
			Interpolate(1);
		}
		else
		{
			Interpolate(2);
		}
		Draw_Grid();
	}

	private void TB_Btn12_Click(object sender, EventArgs e)
	{
		Extrapolate();
		Draw_Grid();
	}

	private void TB_Btn13_Click(object sender, EventArgs e)
	{
		Undo();
		Draw_Grid();
	}

	private void UndoToolStripMenuItem_Click(object sender, EventArgs e)
	{
		Undo();
		((Control)DataMenuStrip).Hide();
		Draw_Grid();
	}

	public void Undo()
	{
		checked
		{
			if (UndoC != 0)
			{
				int num = 1 + (m_Grid_X + 1) * (m_Grid_Y + 1);
				for (int i = 0; i <= num; i++)
				{
					GData[i] = GDataU[i + (UndoC - 1) * (m_Grid_X + 1) * (m_Grid_Y + 1)];
				}
				UndoC--;
				if (UndoC == 0)
				{
					UndoToolStripMenuItem.Enabled = false;
				}
				if (UndoC == 0)
				{
					((Control)TB_Btn13).Enabled = false;
				}
			}
		}
	}

	public void SaveUndo()
	{
		checked
		{
			UndoC++;
			if (UndoC > MAX_U)
			{
				UndoC = (byte)MAX_U;
				int num = MAX_U - 1;
				for (int i = 1; i <= num; i++)
				{
					int num2 = 1 + (m_Grid_X + 1) * (m_Grid_Y + 1);
					for (int j = 0; j <= num2; j++)
					{
						GDataU[j + (i - 1) * (m_Grid_X + 1) * (m_Grid_Y + 1)] = GDataU[j + (i + 1 - 1) * (m_Grid_X + 1) * (m_Grid_Y + 1)];
					}
				}
			}
			int num3 = 1 + (m_Grid_X + 1) * (m_Grid_Y + 1);
			for (int k = 0; k <= num3; k++)
			{
				GDataU[k + (UndoC - 1) * (m_Grid_X + 1) * (m_Grid_Y + 1)] = GData[k];
			}
			UndoToolStripMenuItem.Enabled = true;
			((Control)TB_Btn13).Enabled = true;
		}
	}

	private void ClearUndo()
	{
		UndoC = 0;
		UndoToolStripMenuItem.Enabled = false;
		((Control)TB_Btn13).Enabled = false;
	}

	private void DataMenuStrip_Opening(object sender, CancelEventArgs e)
	{
	}
}
