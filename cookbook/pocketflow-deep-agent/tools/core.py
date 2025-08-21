from abc import abstractmethod
import asyncio
import json
import yaml
from utils import log
from itertools import chain
class Tool:
    in_post = dict(
        context={},
        metadata={},
        chat={},
        memory={}
    )
    in_prep = dict(
        memory={},
        chat={},
    )
    @property
    def schema(self):
        return self.__class__.schema
    def __init__(self, memory,environnement="cli", **kwargs):
        self.memory = memory
        self.kwargs = kwargs
        self.environnement = environnement
        self.prep()
        if self.environnement == "cli":
            self.prep_cli()

    async def execute(self):
        self.result = await self.exec()
        self.metadata = self.metadata(self.result)
        if self.environnement == "cli":
            self.post_cli(self.result)
        self.text = yaml.dump(self.post(self.result))
        self.post_to_memory(self.memory, self.result)

    def prep(self):
        assert tuple(self.schema["parameters"]["required"]) == tuple(self.kwargs.keys())
        
    def prep_cli(self):
        log.info(
            yaml.dump(
                {
                    k: v for k, v in self.in_prep.items() if v
                }
            )
        )
    @abstractmethod
    async def exec(self) -> dict:
        await asyncio.sleep(0)  # Simulate async operation
        return self.kwargs
    def post(self,result):
        return {"ok":True} | {
            k: result.get(k) 
            for k in self.in_post["context"]
        }

    def post_to_memory(self,memory,result):
        memory = memory | {
            k: result.get(k) 
            for k in self.in_post["memory"]
        }
    def post_cli(self,result):
        
        log.info(
            yaml.dump(
                {
                    i: result.get(i) 
                      for i in chain.from_iterable([ outputs for _in, outputs in self.in_post.items() if outputs])

                }
            )
        )
    def metadata(self, result):
        return {
            k: result.get(k) 
            for k in self.in_post["metadata"]
        } | {
            "name" :self.name
        }


