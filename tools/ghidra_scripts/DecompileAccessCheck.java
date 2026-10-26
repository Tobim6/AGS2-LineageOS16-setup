import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Data;
import ghidra.program.model.listing.DataIterator;
import ghidra.program.model.listing.Function;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;
import ghidra.util.task.ConsoleTaskMonitor;
import java.util.LinkedHashSet;
import java.util.Set;

public class DecompileAccessCheck extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] targets = { "native_packages.xml", "set_nativeCA", "hash" };
        DecompInterface decomp = new DecompInterface();
        decomp.openProgram(currentProgram);
        Set<Function> fs = new LinkedHashSet<>();
        DataIterator it = currentProgram.getListing().getDefinedData(currentProgram.getMinAddress(), true);
        while (it.hasNext()) {
            Data d = it.next();
            if (!d.hasStringValue()) continue;
            String v = d.getDefaultValueRepresentation();
            for (String t : targets) {
                if (v.contains(t)) {
                    ReferenceIterator r = currentProgram.getReferenceManager().getReferencesTo(d.getAddress());
                    while (r.hasNext()) {
                        Function f = getFunctionContaining(r.next().getFromAddress());
                        if (f != null) fs.add(f);
                    }
                    break;
                }
            }
        }
        println("=== Found " + fs.size() + " functions ===");
        for (Function f : fs) {
            println("\n==== FUNCTION: " + f.getName() + " @ " + f.getEntryPoint() + " ====");
            DecompileResults res = decomp.decompileFunction(f, 90, new ConsoleTaskMonitor());
            println(res.decompileCompleted() ? res.getDecompiledFunction().getC() : "decompile failed");
        }
        decomp.dispose();
    }
}
