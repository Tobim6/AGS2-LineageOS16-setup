import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;

// ListFuncs [substring...]: print "name @ addr size" for every function (or only those containing a substring).
public class ListFuncs extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] a = getScriptArgs();
        FunctionIterator it = currentProgram.getFunctionManager().getFunctions(true);
        while (it.hasNext()) {
            Function f = it.next();
            boolean ok = a.length == 0;
            for (String s : a) if (f.getName().toLowerCase().contains(s.toLowerCase())) ok = true;
            if (ok) println("FN " + f.getName() + " @ " + f.getEntryPoint() + " size=" + f.getBody().getNumAddresses());
        }
    }
}
