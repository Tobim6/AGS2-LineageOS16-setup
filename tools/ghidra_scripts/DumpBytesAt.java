import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;

public class DumpBytesAt extends GhidraScript {
    @Override
    public void run() throws Exception {
        long[] addrs = { 0x00101d88L, 0x00101950L };
        for (long a : addrs) {
            Address addr = currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(a);
            byte[] buf = new byte[32];
            int n = currentProgram.getMemory().getBytes(addr, buf);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) {
                sb.append(String.format("%02x ", buf[i]));
            }
            println("Address " + addr + " bytes: " + sb.toString());
        }
    }
}
