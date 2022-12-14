value_label_brush = QBrush(Qt.red)

self.IFFlush_label = QGraphicsSimpleTextItem()
self.IFFlush_label.setBrush(value_label_brush)
self.IFFlush_label.setPos(self.object_scale_factor * 46, self.object_scale_factor * 3)
self.IFFlush_label.setText("IFFlush")
self.scene.addItem(self.IFFlush_label)


self.ControlZeroMUXinput_label = QGraphicsSimpleTextItem()
self.ControlZeroMUXinput_label.setBrush(value_label_brush)
self.ControlZeroMUXinput_label.setPos(self.object_scale_factor * 38, self.object_scale_factor * 7)
self.ControlZeroMUXinput_label.setText("ControlZeroMUXinput")
self.scene.addItem(self.ControlZeroMUXinput_label)


self.BranchControl_label = QGraphicsSimpleTextItem()
self.BranchControl_label.setBrush(value_label_brush)
self.BranchControl_label.setPos(self.object_scale_factor * 44, self.object_scale_factor * 7)
self.BranchControl_label.setText("BranchControl")
self.scene.addItem(self.BranchControl_label)


self.JAddrCalcvalue_label = QGraphicsSimpleTextItem()
self.JAddrCalcvalue_label.setBrush(value_label_brush)
self.JAddrCalcvalue_label.setPos(self.object_scale_factor * 29, self.object_scale_factor * 9)
self.JAddrCalcvalue_label.setText("JAddrCalcvalue")
self.scene.addItem(self.JAddrCalcvalue_label)


self.ControlZeroMUXvalue_label = QGraphicsSimpleTextItem()
self.ControlZeroMUXvalue_label.setBrush(value_label_brush)
self.ControlZeroMUXvalue_label.setPos(self.object_scale_factor * 39, self.object_scale_factor * 10)
self.ControlZeroMUXvalue_label.setText("ControlZeroMUXvalue")
self.scene.addItem(self.ControlZeroMUXvalue_label)


self.IFIDWrite_label = QGraphicsSimpleTextItem()
self.IFIDWrite_label.setBrush(value_label_brush)
self.IFIDWrite_label.setPos(self.object_scale_factor * 18, self.object_scale_factor * 11)
self.IFIDWrite_label.setText("IFIDWrite")
self.scene.addItem(self.IFIDWrite_label)


self.ForwardAMUXinput_label = QGraphicsSimpleTextItem()
self.ForwardAMUXinput_label.setBrush(value_label_brush)
self.ForwardAMUXinput_label.setPos(self.object_scale_factor * 60, self.object_scale_factor * 11)
self.ForwardAMUXinput_label.setText("ForwardAMUXinput")
self.scene.addItem(self.ForwardAMUXinput_label)


self.BranchCMPForwardAMUXinput_label = QGraphicsSimpleTextItem()
self.BranchCMPForwardAMUXinput_label.setBrush(value_label_brush)
self.BranchCMPForwardAMUXinput_label.setPos(self.object_scale_factor * 43, self.object_scale_factor * 12)
self.BranchCMPForwardAMUXinput_label.setText("BranchCMPForwardAMUXinput")
self.scene.addItem(self.BranchCMPForwardAMUXinput_label)


self.PC4Addvalue_label = QGraphicsSimpleTextItem()
self.PC4Addvalue_label.setBrush(value_label_brush)
self.PC4Addvalue_label.setPos(self.object_scale_factor * 13, self.object_scale_factor * 13)
self.PC4Addvalue_label.setText("PC4Addvalue")
self.scene.addItem(self.PC4Addvalue_label)


self.IFIDPCvalue_label = QGraphicsSimpleTextItem()
self.IFIDPCvalue_label.setBrush(value_label_brush)
self.IFIDPCvalue_label.setPos(self.object_scale_factor * 22, self.object_scale_factor * 13)
self.IFIDPCvalue_label.setText("IFIDPCvalue")
self.scene.addItem(self.IFIDPCvalue_label)


self.MemRead_label = QGraphicsSimpleTextItem()
self.MemRead_label.setBrush(value_label_brush)
self.MemRead_label.setPos(self.object_scale_factor * 83, self.object_scale_factor * 13)
self.MemRead_label.setText("MemRead")
self.scene.addItem(self.MemRead_label)


self.BranchPCAddervalue_label = QGraphicsSimpleTextItem()
self.BranchPCAddervalue_label.setBrush(value_label_brush)
self.BranchPCAddervalue_label.setPos(self.object_scale_factor * 35, self.object_scale_factor * 14)
self.BranchPCAddervalue_label.setText("BranchPCAddervalue")
self.scene.addItem(self.BranchPCAddervalue_label)


self.ForwardAMUXvalue_label = QGraphicsSimpleTextItem()
self.ForwardAMUXvalue_label.setBrush(value_label_brush)
self.ForwardAMUXvalue_label.setPos(self.object_scale_factor * 61, self.object_scale_factor * 14)
self.ForwardAMUXvalue_label.setText("ForwardAMUXvalue")
self.scene.addItem(self.ForwardAMUXvalue_label)


self.BTAvalue_label = QGraphicsSimpleTextItem()
self.BTAvalue_label.setBrush(value_label_brush)
self.BTAvalue_label.setPos(self.object_scale_factor * 32, self.object_scale_factor * 15)
self.BTAvalue_label.setText("BTAvalue")
self.scene.addItem(self.BTAvalue_label)


self.BranchCMPForwardAMUXvalue_label = QGraphicsSimpleTextItem()
self.BranchCMPForwardAMUXvalue_label.setBrush(value_label_brush)
self.BranchCMPForwardAMUXvalue_label.setPos(self.object_scale_factor * 44, self.object_scale_factor * 15)
self.BranchCMPForwardAMUXvalue_label.setText("BranchCMPForwardAMUXvalue")
self.scene.addItem(self.BranchCMPForwardAMUXvalue_label)


self.BranchEqualCMPvalue_label = QGraphicsSimpleTextItem()
self.BranchEqualCMPvalue_label.setBrush(value_label_brush)
self.BranchEqualCMPvalue_label.setPos(self.object_scale_factor * 47, self.object_scale_factor * 17)
self.BranchEqualCMPvalue_label.setText("BranchEqualCMPvalue")
self.scene.addItem(self.BranchEqualCMPvalue_label)


self.ALUResult_label = QGraphicsSimpleTextItem()
self.ALUResult_label.setBrush(value_label_brush)
self.ALUResult_label.setPos(self.object_scale_factor * 70, self.object_scale_factor * 17)
self.ALUResult_label.setText("ALUResult")
self.scene.addItem(self.ALUResult_label)


self.MemoryWriteaddr_label = QGraphicsSimpleTextItem()
self.MemoryWriteaddr_label.setBrush(value_label_brush)
self.MemoryWriteaddr_label.setPos(self.object_scale_factor * 80, self.object_scale_factor * 17)
self.MemoryWriteaddr_label.setText("MemoryWriteaddr")
self.scene.addItem(self.MemoryWriteaddr_label)


self.ReadReg1_label = QGraphicsSimpleTextItem()
self.ReadReg1_label.setBrush(value_label_brush)
self.ReadReg1_label.setPos(self.object_scale_factor * 32, self.object_scale_factor * 18)
self.ReadReg1_label.setText("ReadReg1")
self.scene.addItem(self.ReadReg1_label)


self.BranchCMPForwardBMUXvalue_label = QGraphicsSimpleTextItem()
self.BranchCMPForwardBMUXvalue_label.setBrush(value_label_brush)
self.BranchCMPForwardBMUXvalue_label.setPos(self.object_scale_factor * 44, self.object_scale_factor * 19)
self.BranchCMPForwardBMUXvalue_label.setText("BranchCMPForwardBMUXvalue")
self.scene.addItem(self.BranchCMPForwardBMUXvalue_label)


self.MemoryReadvalue_label = QGraphicsSimpleTextItem()
self.MemoryReadvalue_label.setBrush(value_label_brush)
self.MemoryReadvalue_label.setPos(self.object_scale_factor * 86, self.object_scale_factor * 19)
self.MemoryReadvalue_label.setText("MemoryReadvalue")
self.scene.addItem(self.MemoryReadvalue_label)


self.PCWrite_label = QGraphicsSimpleTextItem()
self.PCWrite_label.setBrush(value_label_brush)
self.PCWrite_label.setPos(self.object_scale_factor * 7, self.object_scale_factor * 20)
self.PCWrite_label.setText("PCWrite")
self.scene.addItem(self.PCWrite_label)


self.ReadReg2_label = QGraphicsSimpleTextItem()
self.ReadReg2_label.setBrush(value_label_brush)
self.ReadReg2_label.setPos(self.object_scale_factor * 32, self.object_scale_factor * 20)
self.ReadReg2_label.setText("ReadReg2")
self.scene.addItem(self.ReadReg2_label)


self.BranchCMPForwardBMUXinput_label = QGraphicsSimpleTextItem()
self.BranchCMPForwardBMUXinput_label.setBrush(value_label_brush)
self.BranchCMPForwardBMUXinput_label.setPos(self.object_scale_factor * 43, self.object_scale_factor * 20)
self.BranchCMPForwardBMUXinput_label.setText("BranchCMPForwardBMUXinput")
self.scene.addItem(self.BranchCMPForwardBMUXinput_label)


self.ForwardBMUXvalue_label = QGraphicsSimpleTextItem()
self.ForwardBMUXvalue_label.setBrush(value_label_brush)
self.ForwardBMUXvalue_label.setPos(self.object_scale_factor * 61, self.object_scale_factor * 21)
self.ForwardBMUXvalue_label.setText("ForwardBMUXvalue")
self.scene.addItem(self.ForwardBMUXvalue_label)


self.ForwardBMUXinput_label = QGraphicsSimpleTextItem()
self.ForwardBMUXinput_label.setBrush(value_label_brush)
self.ForwardBMUXinput_label.setPos(self.object_scale_factor * 60, self.object_scale_factor * 22)
self.ForwardBMUXinput_label.setText("ForwardBMUXinput")
self.scene.addItem(self.ForwardBMUXinput_label)


self.ALUSrcMUXvalue_label = QGraphicsSimpleTextItem()
self.ALUSrcMUXvalue_label.setBrush(value_label_brush)
self.ALUSrcMUXvalue_label.setPos(self.object_scale_factor * 64, self.object_scale_factor * 22)
self.ALUSrcMUXvalue_label.setText("ALUSrcMUXvalue")
self.scene.addItem(self.ALUSrcMUXvalue_label)


self.RegRead1value_label = QGraphicsSimpleTextItem()
self.RegRead1value_label.setBrush(value_label_brush)
self.RegRead1value_label.setPos(self.object_scale_factor * 38, self.object_scale_factor * 23)
self.RegRead1value_label.setText("RegRead1value")
self.scene.addItem(self.RegRead1value_label)


self.ALUSrcMUXinput_label = QGraphicsSimpleTextItem()
self.ALUSrcMUXinput_label.setBrush(value_label_brush)
self.ALUSrcMUXinput_label.setPos(self.object_scale_factor * 63, self.object_scale_factor * 23)
self.ALUSrcMUXinput_label.setText("ALUSrcMUXinput")
self.scene.addItem(self.ALUSrcMUXinput_label)


self.MemtoRegMUXinput_label = QGraphicsSimpleTextItem()
self.MemtoRegMUXinput_label.setBrush(value_label_brush)
self.MemtoRegMUXinput_label.setPos(self.object_scale_factor * 95, self.object_scale_factor * 23)
self.MemtoRegMUXinput_label.setText("MemtoRegMUXinput")
self.scene.addItem(self.MemtoRegMUXinput_label)


self.PCSrcMUXinput_label = QGraphicsSimpleTextItem()
self.PCSrcMUXinput_label.setBrush(value_label_brush)
self.PCSrcMUXinput_label.setPos(self.object_scale_factor * 4, self.object_scale_factor * 24)
self.PCSrcMUXinput_label.setText("PCSrcMUXinput")
self.scene.addItem(self.PCSrcMUXinput_label)


self.WriteReg_label = QGraphicsSimpleTextItem()
self.WriteReg_label.setBrush(value_label_brush)
self.WriteReg_label.setPos(self.object_scale_factor * 32, self.object_scale_factor * 24)
self.WriteReg_label.setText("WriteReg")
self.scene.addItem(self.WriteReg_label)


self.MemoryWritevalue_label = QGraphicsSimpleTextItem()
self.MemoryWritevalue_label.setBrush(value_label_brush)
self.MemoryWritevalue_label.setPos(self.object_scale_factor * 80, self.object_scale_factor * 24)
self.MemoryWritevalue_label.setText("MemoryWritevalue")
self.scene.addItem(self.MemoryWritevalue_label)


self.PC_label = QGraphicsSimpleTextItem()
self.PC_label.setBrush(value_label_brush)
self.PC_label.setPos(self.object_scale_factor * 7, self.object_scale_factor * 25)
self.PC_label.setText("PC")
self.scene.addItem(self.PC_label)


self.ALUControlvalue_label = QGraphicsSimpleTextItem()
self.ALUControlvalue_label.setBrush(value_label_brush)
self.ALUControlvalue_label.setPos(self.object_scale_factor * 67, self.object_scale_factor * 25)
self.ALUControlvalue_label.setText("ALUControlvalue")
self.scene.addItem(self.ALUControlvalue_label)


self.MemWrite_label = QGraphicsSimpleTextItem()
self.MemWrite_label.setBrush(value_label_brush)
self.MemWrite_label.setPos(self.object_scale_factor * 83, self.object_scale_factor * 25)
self.MemWrite_label.setText("MemWrite")
self.scene.addItem(self.MemWrite_label)


self.WriteRegData_label = QGraphicsSimpleTextItem()
self.WriteRegData_label.setBrush(value_label_brush)
self.WriteRegData_label.setPos(self.object_scale_factor * 32, self.object_scale_factor * 26)
self.WriteRegData_label.setText("WriteRegData")
self.scene.addItem(self.WriteRegData_label)


self.RegRead2value_label = QGraphicsSimpleTextItem()
self.RegRead2value_label.setBrush(value_label_brush)
self.RegRead2value_label.setPos(self.object_scale_factor * 38, self.object_scale_factor * 26)
self.RegRead2value_label.setText("RegRead2value")
self.scene.addItem(self.RegRead2value_label)


self.MemtoRegMUXvalue_label = QGraphicsSimpleTextItem()
self.MemtoRegMUXvalue_label.setBrush(value_label_brush)
self.MemtoRegMUXvalue_label.setPos(self.object_scale_factor * 96, self.object_scale_factor * 26)
self.MemtoRegMUXvalue_label.setText("MemtoRegMUXvalue")
self.scene.addItem(self.MemtoRegMUXvalue_label)


self.Instruction_label = QGraphicsSimpleTextItem()
self.Instruction_label.setBrush(value_label_brush)
self.Instruction_label.setPos(self.object_scale_factor * 13, self.object_scale_factor * 27)
self.Instruction_label.setText("Instruction")
self.scene.addItem(self.Instruction_label)


self.Immediatevalue_label = QGraphicsSimpleTextItem()
self.Immediatevalue_label.setBrush(value_label_brush)
self.Immediatevalue_label.setPos(self.object_scale_factor * 24, self.object_scale_factor * 27)
self.Immediatevalue_label.setText("Immediatevalue")
self.scene.addItem(self.Immediatevalue_label)


self.RegWrite_label = QGraphicsSimpleTextItem()
self.RegWrite_label.setBrush(value_label_brush)
self.RegWrite_label.setPos(self.object_scale_factor * 35, self.object_scale_factor * 27)
self.RegWrite_label.setText("RegWrite")
self.scene.addItem(self.RegWrite_label)


self.ImmSignExtendedvalue_label = QGraphicsSimpleTextItem()
self.ImmSignExtendedvalue_label.setBrush(value_label_brush)
self.ImmSignExtendedvalue_label.setPos(self.object_scale_factor * 30, self.object_scale_factor * 29)
self.ImmSignExtendedvalue_label.setText("ImmSignExtendedvalue")
self.scene.addItem(self.ImmSignExtendedvalue_label)


self.ImmediateSLL16value_label = QGraphicsSimpleTextItem()
self.ImmediateSLL16value_label.setBrush(value_label_brush)
self.ImmediateSLL16value_label.setPos(self.object_scale_factor * 27, self.object_scale_factor * 30)
self.ImmediateSLL16value_label.setText("ImmediateSLL16value")
self.scene.addItem(self.ImmediateSLL16value_label)


self.RegDstMUXvalue_label = QGraphicsSimpleTextItem()
self.RegDstMUXvalue_label.setBrush(value_label_brush)
self.RegDstMUXvalue_label.setPos(self.object_scale_factor * 62, self.object_scale_factor * 33)
self.RegDstMUXvalue_label.setText("RegDstMUXvalue")
self.scene.addItem(self.RegDstMUXvalue_label)


self.RegDstMUXinput_label = QGraphicsSimpleTextItem()
self.RegDstMUXinput_label.setBrush(value_label_brush)
self.RegDstMUXinput_label.setPos(self.object_scale_factor * 61, self.object_scale_factor * 34)
self.RegDstMUXinput_label.setText("RegDstMUXinput")
self.scene.addItem(self.RegDstMUXinput_label)

