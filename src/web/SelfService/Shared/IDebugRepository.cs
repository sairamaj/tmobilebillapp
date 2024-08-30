using System.Collections.Generic;
using System.Threading.Tasks;
using SelfService.Shared;

namespace SelfService.Shared
{
    public interface IDebugRepository
    {
        Task<DebugInfo> GetDebugInfo();
    }
}