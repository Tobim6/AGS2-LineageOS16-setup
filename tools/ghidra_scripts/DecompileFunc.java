import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionIterator;
import ghidra.util.task.ConsoleTaskMonitor;

// Decompile functions whose name contains any script argument.
public class DecompileFunc extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] targets = getScriptArgs();
        DecompInterface decomp = new DecompInterface();
        decomp.openProgram(currentProgram);
        FunctionIterator it = currentProgram.getFunctionManager().getFunctions(true);
        while (it.hasNext()) {
            Function f = it.next();
            for (String t : targets) {
                if (f.getName().contains(t)) {
                    println("\n==== FUNCTION: " + f.getName() + " @ " + f.getEntryPoint() + " ====");
                    DecompileResults res = decomp.decompileFunction(f, 120, new ConsoleTaskMonitor());
                    println(res.decompileCompleted() ? res.getDecompiledFunction().getC() : "decompile failed");
                    break;
                }
            }
        }
        decomp.dispose();
    }
}
