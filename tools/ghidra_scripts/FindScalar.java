import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import ghidra.program.model.scalar.Scalar;
import ghidra.program.model.address.Address;

// FindScalar <function-name-substring> <hex scalar>: print instructions in matching functions that use the scalar.
public class FindScalar extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] a = getScriptArgs();
        long want = Long.decode(a[1]);
        FunctionIterator fit = currentProgram.getFunctionManager().getFunctions(true);
        while (fit.hasNext()) {
            Function f = fit.next();
            if (!f.getName().contains(a[0])) continue;
            InstructionIterator it = currentProgram.getListing().getInstructions(f.getBody(), true);
            while (it.hasNext()) {
                Instruction ins = it.next();
                for (int i = 0; i < ins.getNumOperands(); i++) {
                    Object[] objs = ins.getOpObjects(i);
                    for (Object o : objs) {
                        if (o instanceof Scalar && ((Scalar) o).getUnsignedValue() == want) {
                            StringBuilder sb = new StringBuilder();
                            for (byte b : ins.getBytes()) sb.append(String.format("%02x", b & 0xff));
                            long fileoff = currentProgram.getMemory().getAddressSourceInfo(ins.getAddress()) != null
                                ? currentProgram.getMemory().getAddressSourceInfo(ins.getAddress()).getFileOffset() : -1;
                            println("HIT " + f.getName() + " @ " + ins.getAddress() + " fileoff=0x" + Long.toHexString(fileoff) + " bytes=" + sb + " : " + ins);
                        }
                    }
                }
            }
        }
    }
}
