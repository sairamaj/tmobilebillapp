using System;
using System.Threading.Tasks;

namespace SelfService.Shared
{
    public interface ICacheManager
    {
        Task<T> GetWithSet<T>(string key, TimeSpan expiry, Func<Task<T>> func);
    }
}